import django
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.views.generic import View, TemplateView
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from wagtail.contrib.modeladmin.views import IndexView

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import set_consent
from wagtail_tag_manager.models import Constant, Variable, TagTypeSettings
from wagtail_tag_manager.webdriver import CookieScanner
from wagtail_tag_manager.decorators import get_variables

__version__ = django.get_version()


class ManageView(SuccessURLAllowedHostsMixin, TemplateView):
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
        if __version__.startswith("2.0"):
            kwargs["allowed_hosts"] = allowed_hosts
        else:
            args.append(allowed_hosts)

        url_is_safe = is_safe_url(*args, **kwargs)
        if url_is_safe:
            response = HttpResponseRedirect(redirect_url)

        form = ConsentForm(request.POST)
        if form.is_valid():
            set_consent(
                response,
                {key: str(value).lower() for key, value in form.cleaned_data.items()},
            )

        return response


class ConfigView(View):
    def get(self, request, *args, **kwargs):
        response = JsonResponse(
            {
                tag_type: config.get("value")
                for tag_type, config in TagTypeSettings.all().items()
            }
        )

        return response


class VariableView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return JsonResponse(
                {
                    "constants": [
                        constant.as_dict() for constant in Constant.objects.all()
                    ],
                    "variables": [
                        *[variable.as_dict() for variable in get_variables()],
                        *[variable.as_dict() for variable in Variable.objects.all()],
                    ],
                }
            )
        return HttpResponseNotFound()


class CookieDeclarationIndexView(IndexView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            response = HttpResponseRedirect("")
            CookieScanner(request).scan()
            return response

        return HttpResponseNotFound()
