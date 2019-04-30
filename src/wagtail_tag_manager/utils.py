import typing
from datetime import datetime, timedelta

import django
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.cache import patch_vary_headers

from wagtail_tag_manager.settings import TagTypeSettings
from wagtail_tag_manager.strategy import CONSENT_UNSET

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


def get_page_for_request(request):
    if request and hasattr(request, "site"):
        path = request.path
        path_components = [component for component in path.split("/") if component]
        page, args, kwargs = request.site.root_page.specific.route(
            request, path_components
        )
        return page

    return None
