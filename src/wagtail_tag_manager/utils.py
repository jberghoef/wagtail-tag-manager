import uuid
import typing
from datetime import datetime, timedelta

import django
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.cache import patch_vary_headers

from wagtail_tag_manager.models import CookieConsent
from wagtail_tag_manager.settings import TagTypeSettings, CookieConsentSettings
from wagtail_tag_manager.strategy import CONSENT_UNSET

__version__ = django.get_version()


def set_consent(request, response, consent, explicit=False):
    consent_state = {**get_consent(response), **consent}
    _set_cookie(
        response,
        "wtm",
        "|".join(["{}:{}".format(key, value) for key, value in consent_state.items()]),
    )

    if request is not None and explicit:
        cookie_consent = CookieConsent.objects.create(
            identifier=request.COOKIES.get("wtm_id", str(uuid.uuid4())),
            consent_state="\n".join(
                ["{}: {};".format(key, value) for key, value in consent_state.items()]
            ),
            location=request.META.get("HTTP_REFERER", request.build_absolute_uri()),
        )
        _set_cookie(response, "wtm_id", cookie_consent.identifier)


def get_consent(r: typing.Union[HttpResponse, HttpRequest]):
    cookies = getattr(r, "COOKIES", {})
    if isinstance(r, HttpResponse):
        cookies = {
            key: getattr(r, "cookies", {}).get(key).value
            for key in getattr(r, "cookies", {}).keys()
        }

    wtm_cookie = cookies.get("wtm", "")
    consent_state = _parse_consent_state(wtm_cookie)

    wtm_id_cookie = cookies.get("wtm_id", "")
    if not _validate_given_consent(wtm_id_cookie, r):
        consent_state = _parse_consent_state("")

    return consent_state


def _validate_given_consent(
    consent_id: str, r: typing.Union[HttpResponse, HttpRequest]
):
    if consent_id:
        settings = CookieConsentSettings.for_request(r)
        consent = (
            CookieConsent.objects.filter(identifier=consent_id)
            .order_by("timestamp")
            .last()
        )

        invalidation_timestamp = settings.get_timestamp()
        if consent and invalidation_timestamp:
            return consent.timestamp > invalidation_timestamp

    return True


def _parse_consent_state(cookie_value: str) -> dict:
    consent_state = {tag_type: CONSENT_UNSET for tag_type in TagTypeSettings.all()}
    consent_state.update(
        {
            item.split(":")[0]: item.split(":")[1]
            for item in cookie_value.split("|")
            if ":" in item
        }
    )
    return consent_state


def _set_cookie(response, key, value, days_expire=None):
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
        "samesite": "Lax",
        "httponly": False,
    }

    response.set_cookie(key, value, **kwargs)
    patch_vary_headers(response, ("Cookie",))

    return response


def get_page_for_request(request):
    site = get_site_for_request(request)
    if site:
        path = request.path
        path_components = [component for component in path.split("/") if component]
        page, args, kwargs = site.root_page.specific.route(request, path_components)
        return page

    return None


def get_site_for_request(request):
    try:
        from wagtail.core.models import Site

        return Site.find_for_request(request)
    except:  # noqa: E722
        return getattr(request, "site")
