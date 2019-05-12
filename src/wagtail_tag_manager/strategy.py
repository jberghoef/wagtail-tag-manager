from typing import Dict, List

from django.http import Http404, HttpRequest
from django.db.models import Q
from wagtail.core.views import serve as wagtail_serve

from wagtail_tag_manager.mixins import TagMixin
from wagtail_tag_manager.models import Tag, Trigger, TagTypeSettings
from wagtail_tag_manager.settings import (
    SETTING_DEFAULT,
    SETTING_DELAYED,
    SETTING_INITIAL,
    SETTING_REQUIRED,
)

CONSENT_TRUE = "true"
CONSENT_FALSE = "false"
CONSENT_UNSET = "unset"

CONSENT_MAP = (
    # Method, tag config
    (
        "GET",
        SETTING_REQUIRED,
        (
            # Consent validator, consent value, include instant tags, include lazy tags
            (lambda c: True, CONSENT_TRUE, True, False),
        ),
    ),
    (
        "GET",
        SETTING_INITIAL,
        (
            (lambda c: c == CONSENT_UNSET, CONSENT_UNSET, False, False),
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, True, False),
        ),
    ),
    (
        "GET",
        SETTING_DELAYED,
        (
            (lambda c: c == CONSENT_UNSET, CONSENT_UNSET, False, False),
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, True, False),
        ),
    ),
    (
        "GET",
        SETTING_DEFAULT,
        (
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, True, False),
            (lambda c: c != CONSENT_TRUE, CONSENT_FALSE, False, False),
        ),
    ),
    ("POST", SETTING_REQUIRED, ((lambda c: True, CONSENT_TRUE, False, True),)),
    (
        "POST",
        SETTING_INITIAL,
        (
            (lambda c: c == CONSENT_UNSET, CONSENT_UNSET, True, True),
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, False, True),
        ),
    ),
    (
        "POST",
        SETTING_DELAYED,
        (
            (lambda c: c == CONSENT_UNSET, CONSENT_TRUE, False, False),
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, False, True),
        ),
    ),
    (
        "POST",
        SETTING_DEFAULT,
        (
            (lambda c: c == CONSENT_TRUE, CONSENT_TRUE, False, True),
            (lambda c: c != CONSENT_TRUE, CONSENT_FALSE, False, False),
        ),
    ),
)


class TagStrategy(object):
    def __init__(self, request: HttpRequest, payload: dict = None):
        self._request = request
        self._context = Tag.create_context(request)
        self._payload = payload or {}

        self._config = TagTypeSettings.all()
        self._tags: List = []

        from wagtail_tag_manager.utils import get_consent

        self.consent_state = get_consent(request)
        self.consent: Dict = {}

        if request:
            self.define_strategy()

    # https://gist.github.com/jberghoef/9ffa2b738cbb0aab624ff091dc6fe9a7
    def define_strategy(self):
        for method in (
            [self._request.method] if not self.is_trigger else ["GET", "POST"]
        ):
            for tag_type, tag_config in self._config.items():
                consent_value, include_instant, include_lazy = self.validate_request(
                    method, tag_type, tag_config
                )

                self.consent[tag_type] = consent_value

                if include_instant:
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))

                if include_lazy:
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

    def validate_request(self, method: str, tag_type: str, tag_config: dict):
        consent = self.consent_state.get(tag_type, CONSENT_UNSET)
        config = tag_config.get("value")

        for rule in CONSENT_MAP:
            if rule[0] == method and rule[1] == config:
                for validator in rule[2]:
                    if validator[0](consent):
                        return validator[1:]

        return consent, False, False

    def should_include(self, tag_type, tag_config):
        consent = self.consent_state.get(tag_type, CONSENT_UNSET)
        config = tag_config.get("value")

        if config == SETTING_REQUIRED:
            return True
        elif config == SETTING_INITIAL:
            if consent == CONSENT_UNSET or consent == CONSENT_TRUE:
                return True
        elif consent == CONSENT_TRUE:
            return True

        return False

    @property
    def queryset(self):
        queryset = Q()
        for tag_type in self._tags:
            queryset.add(Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1]), Q.OR)
        return queryset

    @property
    def tags(self):
        method = self._request.method
        if self.is_debug and method == "GET":
            return Tag.objects.all()
        elif not self.is_debug and self._tags:
            return Tag.objects.auto_load().filter(self.queryset)

        return Tag.objects.none()

    @property
    def result(self):
        result = []

        if not self.is_trigger:
            result = [*self._get_tags_for_request(), *self._get_tags_for_page()]
        else:
            result = [*self._get_tags_for_trigger()]

        return result

    def _get_tags_for_request(self):
        return [
            {"object": tag, "element": tag.get_doc(self._request, self._context)}
            for tag in self.tags
        ]

    def _get_tags_for_page(self):
        from wagtail_tag_manager.utils import get_page_for_request
        from wagtail_tag_manager.endpoints import lazy_endpoint

        result = []

        if (
            self._request.resolver_match
            and self._request.resolver_match.func == wagtail_serve
            or self._request.resolver_match
            and self._request.resolver_match.func == lazy_endpoint
        ):
            try:
                page = get_page_for_request(self._request)

                if page is not None and isinstance(page, TagMixin):
                    for tag in page.tags.filter(self.queryset):
                        result.append(
                            {
                                "object": tag,
                                "element": tag.get_doc(self._request, self._context),
                            }
                        )
            except Http404:
                pass

        return result

    def _get_tags_for_trigger(self):
        trigger_dict = self._payload.get("trigger")
        trigger = Trigger.objects.get(
            slug=trigger_dict.get("slug"),
            trigger_type__startswith=trigger_dict.get("type"),
        )
        trigger_context = {
            **self._context,
            "trigger_name": trigger_dict.get("slug", ""),
            "trigger_type": trigger_dict.get("type", ""),
            "trigger_value": trigger_dict.get("value", ""),
        }

        if trigger is not None and trigger.validate(trigger_context):
            return [
                {"object": tag, "element": tag.get_doc(self._request, trigger_context)}
                for tag in trigger.tags.filter(self.queryset)
            ]

        return []

    @property
    def cookie_state(self):
        return {
            tag_type: self.consent.get(tag_type, CONSENT_FALSE) != CONSENT_FALSE
            for tag_type in Tag.get_types()
        }

    @property
    def is_debug(self):
        return self._request.COOKIES.get("wtm_debug", "false") == "true"

    @property
    def is_trigger(self):
        return self._payload.get("trigger", None) is not None
