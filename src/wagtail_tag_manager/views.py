import time
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.views.generic import View, TemplateView
from django.utils.http import is_safe_url
from selenium import webdriver
from wagtail.contrib.modeladmin.views import IndexView

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import (
    Constant,
    Variable,
    TagTypeSettings,
    Tag,
    CookieDeclaration,
)


class ManageView(TemplateView):
    template_name = "wagtail_tag_manager/manage.html"

    def get(self, request, *args, **kwargs):
        if getattr(settings, "WTM_MANAGE_VIEW", True):
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect("/")

        redirect_url = request.META.get("HTTP_REFERER", request.build_absolute_uri())
        url_is_safe = is_safe_url(
            redirect_url, settings.ALLOWED_HOSTS, require_https=request.is_secure()
        )
        if url_is_safe:
            response = HttpResponseRedirect(redirect_url)

        form = ConsentForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                set_cookie(response, f"wtm_{key}", str(value).lower())

        return response


class StateView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(TagTypeSettings.all())


class VariableView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return JsonResponse(
                {
                    "constants": [
                        constant.as_dict() for constant in Constant.objects.all()
                    ],
                    "variables": [
                        variable.as_dict() for variable in Variable.objects.all()
                    ],
                }
            )
        return HttpResponseNotFound()


class CookieDeclarationIndexView(IndexView):
    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = HttpResponseRedirect("")

            try:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")

                browser = webdriver.Chrome(options=options)
                browser.implicitly_wait(30)
                browser.get(request.site.root_page.full_url)
                browser.delete_all_cookies()
                for tag in Tag.get_types():
                    browser.add_cookie(
                        {
                            "name": Tag.get_cookie_name(tag),
                            "value": "true",
                            "path": "/",
                            "secure": False,
                        }
                    )
                browser.get(request.site.root_page.full_url)
                time.sleep(10)

                created = 0
                updated = 0

                for cookie in browser.get_cookies():
                    obj, created = CookieDeclaration.objects.update_or_create(
                        name=cookie.get("name"),
                        domain=cookie.get("domain"),
                        defaults={
                            "security": CookieDeclaration.INSECURE_COOKIE
                            if cookie.get("httpOnly")
                            else CookieDeclaration.SECURE_COOKIE
                        },
                    )

                    if created:
                        created = created + 1
                    else:
                        updated = updated + 1

                messages.success(
                    request,
                    _("Created %d declaration(s) and updated %d." % (created, updated)),
                )
            except NotADirectoryError:
                messages.warning(
                    request,
                    mark_safe(
                        _(
                            "Could not instantiate WebDriver session. Please ensure "
                            "<a href='http://chromedriver.chromium.org/' target='_blank' rel='noopener'>ChromeDriver</a> "
                            "is installed and available in your path."
                        )
                    ),
                )
            except Exception as e:
                messages.error(request, e)

            if browser:
                browser.quit()

            return response

        return HttpResponseNotFound()
