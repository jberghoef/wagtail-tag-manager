from datetime import datetime, timedelta

from selenium import webdriver
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.cache import patch_vary_headers
from django.utils.translation import ugettext_lazy as _

from wagtail_tag_manager.models import Tag, CookieDeclaration
from wagtail_tag_manager.strategy import CONSENT_TRUE
from wagtail_tag_manager.settings import TagTypeSettings


def set_cookie(response, key, value, days_expire=None):
    consent_state = get_cookie(response)
    consent_state[key] = str(value).lower()

    if days_expire is None:
        expires = getattr(settings, "WTM_COOKIE_EXPIRE", 365)
        max_age = expires * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    delta = datetime.utcnow() + timedelta(seconds=max_age)
    expires = datetime.strftime(delta, "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(
        "wtm",
        "|".join([f"{key}:{value or 'none'}" for key, value in consent_state.items()]),
        max_age=max_age,
        expires=expires,
        domain=getattr(settings, "SESSION_COOKIE_DOMAIN"),
        secure=getattr(settings, "SESSION_COOKIE_SECURE", None),
        httponly=False,
        samesite="Lax",
    )
    patch_vary_headers(response, ("Cookie",))

    return response


def get_cookie(r):
    cookies = getattr(r, "COOKIES", {})
    if issubclass(r.__class__, HttpResponse):
        response_cookies = getattr(r, "cookies", {})
        cookies = {
            key: response_cookies.get(key).value for key in response_cookies.keys()
        }

    wtm_cookie = cookies.get("wtm", "")
    consent_state = {tag_type: "" for tag_type in TagTypeSettings.all()}
    consent_state.update(
        {
            item.split(":")[0]: item.split(":")[1]
            for item in wtm_cookie.split("|")
            if ":" in item
        }
    )
    return consent_state


def scan_cookies(request):  # pragma: no cover
    def chop_microseconds(delta):
        return delta - timedelta(microseconds=delta.microseconds)

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(30)
        browser.get(request.site.root_page.full_url)
        browser.delete_all_cookies()

        # TODO: Fix this!
        for tag in Tag.get_types():
            browser.add_cookie(
                {
                    "name": Tag.get_cookie_name(tag),
                    "value": CONSENT_TRUE,
                    "path": "",
                    "secure": False,
                }
            )

        browser.get(request.site.root_page.full_url)
        now = datetime.utcnow()

        created = 0
        updated = 0

        for cookie in browser.get_cookies():
            expiry = datetime.fromtimestamp(cookie.get("expiry", now))

            obj, created = CookieDeclaration.objects.update_or_create(
                name=cookie.get("name"),
                domain=cookie.get("domain"),
                defaults={
                    "security": CookieDeclaration.INSECURE_COOKIE
                    if cookie.get("httpOnly")
                    else CookieDeclaration.SECURE_COOKIE,
                    "purpose": _("Unknown"),
                    "duration": chop_microseconds(expiry - now),
                },
            )

            if created:
                created = created + 1
            else:
                updated = updated + 1

        browser.quit()

        messages.success(
            request, _("Created %d declaration(s) and updated %d." % (created, updated))
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
