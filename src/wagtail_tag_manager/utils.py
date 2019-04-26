import django
import typing

from datetime import datetime, timedelta

from selenium import webdriver
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.utils.html import mark_safe
from django.utils.cache import patch_vary_headers
from django.utils.translation import ugettext_lazy as _

from wagtail_tag_manager.models import Tag, CookieDeclaration
from wagtail_tag_manager.strategy import CONSENT_UNSET
from wagtail_tag_manager.settings import TagTypeSettings

__version__ = django.get_version()


def set_consent(response, consent):
    consent_state = {**get_consent(response), **consent}

    set_cookie(
        response,
        "wtm",
        "|".join([f"{key}:{value}" for key, value in consent_state.items()]),
    )


def get_consent(r: typing.Union[HttpResponse, HttpRequest]):
    cookies = getattr(r, "COOKIES", {})
    if isinstance(r, HttpResponse):
        cookies = {
            key: getattr(r, "cookies", {}).get(key).value
            for key in getattr(r, "cookies", {}).keys()
        }

    wtm_cookie = cookies.get("wtm", "")
    consent_state = parse_consent_state(wtm_cookie)

    return consent_state


def parse_consent_state(cookie_value: str) -> dict:
    consent_state = {tag_type: CONSENT_UNSET for tag_type in TagTypeSettings.all()}
    consent_state.update(
        {
            item.split(":")[0]: item.split(":")[1]
            for item in cookie_value.split("|")
            if ":" in item
        }
    )
    return consent_state


def set_cookie(response, key, value, days_expire=None):
    if days_expire is None:
        expires = getattr(settings, "WTM_COOKIE_EXPIRE", 365)
        max_age = expires * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    delta = datetime.utcnow() + timedelta(seconds=max_age)
    expires = datetime.strftime(delta, "%a, %d-%b-%Y %H:%M:%S GMT")

    kwargs = {
        "max_age": max_age,
        "expires": expires,
        "domain": getattr(settings, "SESSION_COOKIE_DOMAIN"),
        "secure": getattr(settings, "SESSION_COOKIE_SECURE", None),
        "httponly": False,
    }

    if not __version__.startswith("2.0"):
        kwargs["samesite"] = "Lax"

    response.set_cookie(key, value, **kwargs)
    patch_vary_headers(response, ("Cookie",))

    return response


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

        browser.add_cookie(
            {
                "name": "wtm",
                "value": "|".join([f"{tag_type}:true" for tag_type in Tag.get_types()]),
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
