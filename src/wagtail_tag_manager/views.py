from django.conf import settings
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.views.generic import View, TemplateView
from wagtail.contrib.modeladmin.views import IndexView

from wagtail_tag_manager.decorators import get_variables
from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import set_consent, scan_cookies
from wagtail_tag_manager.models import Constant, Variable, TagTypeSettings


class ManageView(SuccessURLAllowedHostsMixin, TemplateView):
    template_name = "wagtail_tag_manager/manage.html"

    def get(self, request, *args, **kwargs):
        if getattr(settings, "WTM_MANAGE_VIEW", True):
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect("/")

        redirect_url = request.META.get("HTTP_REFERER", request.build_absolute_uri())
        url_is_safe = is_safe_url(
            redirect_url,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=request.is_secure()
        )
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"cookie_scan_enabled": getattr(settings, "WTM_COOKIE_SCAN", False)}
        )
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            response = HttpResponseRedirect("")
            scan_cookies(request)
            return response

        return HttpResponseNotFound()
