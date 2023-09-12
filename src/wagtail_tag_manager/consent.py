import re
import uuid
from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse

from wagtail_tag_manager.utils import base64_to_dict, dict_to_base64


class Consent(object):
    def __init__(self, request: HttpRequest):
        from wagtail_tag_manager.settings import TagTypeSettings
        from wagtail_tag_manager.strategy import CONSENT_UNSET

        self._now = datetime.utcnow()
        self._request = request
        self._meta = {}
        self._state = {tag_type: CONSENT_UNSET for tag_type in TagTypeSettings.all()}

        self._changed = False

        if self._detect_legacy_consent():
            self._changed = True
            self._load_legacy_consent()
        else:
            self._load_consent()

    def _load_consent(self):
        cookies = getattr(self._request, "COOKIES", {})
        cookie = cookies.get("wtm", "")
        cookie_content = base64_to_dict(cookie) if cookie else {}

        self._meta.update(cookie_content.get("meta", {}))
        if self._has_valid_consent(self._meta.get("id", "")):
            self._state.update(cookie_content.get("state", {}))

    def _detect_legacy_consent(self) -> bool:
        cookies = getattr(self._request, "COOKIES", {})
        legacy_state_cookie = cookies.get("wtm", "")
        if (
            re.fullmatch(r"^(\w+:(true|false|unset|pending)\|?)+$", legacy_state_cookie)
            is not None
        ):
            return True
        return False

    def _load_legacy_consent(self):
        cookies = getattr(self._request, "COOKIES", {})
        legacy_state_cookie = cookies.get("wtm", "")
        self._state.update(
            {
                item.split(":")[0]: item.split(":")[1]
                for item in legacy_state_cookie.split("|")
                if ":" in item
            }
        )

        legacy_meta_cookie = cookies.get("wtm_id", "")
        if legacy_meta_cookie != "":
            self._meta["id"] = legacy_meta_cookie

    def apply_state(self, state: dict):
        if state != self._state:
            self._changed = True
            self._state.update(state)

    def get_meta(self) -> dict:
        return self._meta

    def get_state(self) -> dict:
        return self._state

    def refresh_consent(self, response: HttpResponse) -> HttpResponse:
        from django.conf import settings

        expires = getattr(settings, "WTM_COOKIE_REFRESH", 30)
        max_age = expires * 24 * 60 * 60  # 30 days

        if (
            self._changed
            or self._meta.get("refresh_timestamp", 0)
            < (self._now - timedelta(seconds=max_age)).timestamp()
        ):
            self._meta["refresh_timestamp"] = self._now.timestamp()
            return self._set_cookie(response)

    def set_consent(self, response: HttpResponse) -> HttpResponse:
        self._meta["id"] = self._register_consent().identifier
        self._meta["set_timestamp"] = self._now.timestamp()
        return self._set_cookie(response)

    def _set_cookie(self, response: HttpResponse) -> HttpResponse:
        from django.conf import settings

        expires = getattr(settings, "WTM_COOKIE_EXPIRE", 365)
        max_age = expires * 24 * 60 * 60  # one year

        delta = self._now + timedelta(seconds=max_age)
        expires = datetime.strftime(delta, "%a, %d-%b-%Y %H:%M:%S GMT")

        response.set_cookie(
            "wtm",
            dict_to_base64(
                {
                    "meta": self._meta,
                    "state": self._state,
                }
            ),
            max_age=max_age,
            expires=expires,
            domain=getattr(settings, "SESSION_COOKIE_DOMAIN"),
            secure=getattr(settings, "SESSION_COOKIE_SECURE", None),
            samesite="Lax",
            httponly=False,
        )

        return response

    def _register_consent(self):
        from wagtail_tag_manager.models import CookieConsent

        return CookieConsent.objects.create(
            identifier=self._meta.get("id", str(uuid.uuid4())),
            consent_state="\n".join(
                ["{}: {};".format(key, value) for key, value in self._state.items()]
            ),
            location=self._request.META.get(
                "HTTP_REFERER", self._request.build_absolute_uri()
            ),
        )

    def _has_valid_consent(self, id: str) -> bool:
        """
        This function will check if the CookieConsentSettings have been changed since the last time the user has given consent.
        """
        from wagtail_tag_manager.models import CookieConsent
        from wagtail_tag_manager.settings import CookieConsentSettings

        if id:
            settings = CookieConsentSettings.for_request(self._request)
            consent = (
                CookieConsent.objects.filter(identifier=id).order_by("timestamp").last()
            )

            invalidation_timestamp = settings.get_timestamp()
            if consent and invalidation_timestamp:
                return consent.timestamp > invalidation_timestamp

        return True


class ResponseConsent(object):
    def __init__(self, response: HttpResponse):
        from wagtail_tag_manager.settings import TagTypeSettings
        from wagtail_tag_manager.strategy import CONSENT_UNSET

        self._response = response
        self._meta = {"id": "", "set_timestamp": 0, "refresh_timestamp": 0}
        self._state = {tag_type: CONSENT_UNSET for tag_type in TagTypeSettings.all()}

        self._load_consent()

    def _load_consent(self):
        cookies = {
            key: getattr(self._response, "cookies", {}).get(key).value
            for key in getattr(self._response, "cookies", {}).keys()
        }
        cookie = cookies.get("wtm", "")
        cookie_content = base64_to_dict(cookie) if cookie else {}

        self._meta.update(cookie_content.get("meta", {}))
        self._state.update(cookie_content.get("state", {}))

    def get_meta(self) -> dict:
        return self._meta

    def get_state(self) -> dict:
        return self._state
