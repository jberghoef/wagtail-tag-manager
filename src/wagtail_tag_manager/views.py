from itertools import groupby

import django
from django import forms
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.contrib.auth.views import RedirectURLMixin
from wagtail_modeladmin.views import IndexView

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.models import Trigger, Constant, Variable, TagTypeSettings
from wagtail_tag_manager.consent import Consent
from wagtail_tag_manager.webdriver import CookieScanner
from wagtail_tag_manager.decorators import get_variables

__version__ = django.get_version()
if __version__.startswith("2"):
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class ManageView(RedirectURLMixin, TemplateView):
    template_name = "wagtail_tag_manager/manage.html"

    def get(self, request, *args, **kwargs):
        if (
            getattr(settings, "WTM_MANAGE_VIEW", True)
            or request.COOKIES.get("wtm_debug", "false") == "true"
        ):
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect("/")

        redirect_url = request.META.get("HTTP_REFERER", request.build_absolute_uri())

        args = [redirect_url]
        kwargs = {"require_https": request.is_secure()}

        allowed_hosts = self.get_success_url_allowed_hosts()
        args.append(allowed_hosts)

        if __version__.startswith("2"):
            from django.utils.http import is_safe_url

            url_is_safe = is_safe_url(*args, **kwargs)
        else:
            from django.utils.http import url_has_allowed_host_and_scheme

            url_is_safe = url_has_allowed_host_and_scheme(*args, **kwargs)

        if url_is_safe:
            response = HttpResponseRedirect(redirect_url)

        form = ConsentForm(request.POST)
        if form.is_valid():
            consent = Consent(request)
            consent.apply_state(
                {key: str(value).lower() for key, value in form.cleaned_data.items()}
            )
            consent.set_consent(response)

        return response


class ConfigView(View):
    def get(self, request, *args, **kwargs):
        response = JsonResponse(
            {
                "tag_types": {
                    tag_type: config.get("value")
                    for tag_type, config in TagTypeSettings.all().items()
                },
                "triggers": [trigger.as_dict() for trigger in Trigger.objects.active()],
            }
        )
        return response


class VariableView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound()

    def get(self, request, *args, **kwargs):
        data = []

        if Constant.objects.exists():
            data.append(
                {
                    "verbose_name": _("Constants"),
                    "items": [
                        constant.as_dict() for constant in Constant.objects.all()
                    ],
                }
            )

        if Variable.objects.exists():
            data.append(
                {
                    "verbose_name": _("Variables"),
                    "items": [
                        variable.as_dict() for variable in Variable.objects.all()
                    ],
                }
            )

        custom = [variable.as_dict() for variable in get_variables()]
        custom = sorted(custom, key=lambda x: (x["group"], x["lazy_only"]))
        for key, value in groupby(custom, key=lambda x: x["group"]):
            data.append({"verbose_name": key, "items": list(value)})

        return JsonResponse(data, safe=False)


class WTMIndexView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_text"] = getattr(self.model_admin, "help_text", None)
        return context

    @property
    def media(self):
        return forms.Media(
            css={
                "all": [
                    "wagtail_tag_manager/index.bundle.css",
                    *self.model_admin.get_index_view_extra_css(),
                ]
            },
            js=[
                "wagtail_tag_manager/index.bundle.js",
                *self.model_admin.get_index_view_extra_js(),
            ],
        )


class CookieDeclarationIndexView(WTMIndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scanner_enabled"] = getattr(settings, "WTM_ENABLE_SCANNER", False)
        return context

    def post(self, request, *args, **kwargs):
        if (
            getattr(settings, "WTM_ENABLE_SCANNER", False)
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            response = HttpResponseRedirect("")
            CookieScanner(request).scan()
            return response

        return HttpResponseNotFound()
