from django.db.models import Q

from wagtail_tag_manager.models import Tag, Trigger, TagTypeSettings
from wagtail_tag_manager.settings import (
    SETTING_INITIAL,
    SETTING_CONTINUE,
    SETTING_REQUIRED,
)

CONSENT_TRUE = "true"
CONSENT_FALSE = "false"
CONSENT_UNSET = "unset"


class TagStrategy(object):
    def __init__(self, request):
        self._request = request
        self._context = Tag.create_context(request)

        self._config = TagTypeSettings.all()
        self._tags = []

        from wagtail_tag_manager.utils import get_consent

        self.consent_state = get_consent(request)
        self.consent = {}

        if request:
            self.define_strategy()

    # https://gist.github.com/jberghoef/9ffa2b738cbb0aab624ff091dc6fe9a7
    def define_strategy(self):
        for tag_type, tag_config in self._config.items():
            handler = getattr(self, self._request.method.lower(), None)
            if handler:
                handler(tag_type, tag_config)

    def get(self, tag_type, tag_config):
        consent = self.consent_state.get(tag_type, CONSENT_UNSET)

        if tag_config.get("value") == SETTING_REQUIRED:
            # Include required instant tags
            # Include required cookie
            self._tags.append((Tag.INSTANT_LOAD, tag_type))
            self.consent[tag_type] = CONSENT_TRUE

        elif tag_config.get("value") == SETTING_INITIAL:
            if consent == CONSENT_UNSET:
                # Include initial cookie
                self.consent[tag_type] = CONSENT_UNSET
            elif consent == CONSENT_TRUE:
                # Include initial instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.consent[tag_type] = CONSENT_TRUE

        elif tag_config.get("value") == SETTING_CONTINUE:
            if consent == CONSENT_UNSET:
                # Include initial cookie
                self.consent[tag_type] = CONSENT_UNSET
            elif consent == CONSENT_TRUE:
                # Include initial instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.consent[tag_type] = CONSENT_TRUE

        else:
            if consent == CONSENT_TRUE:
                # Include generic instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.consent[tag_type] = CONSENT_TRUE

    def post(self, tag_type, tag_config):
        consent = self.consent_state.get(tag_type, CONSENT_UNSET)

        if tag_config.get("value") == SETTING_REQUIRED:
            # Include required lazy tags
            # Include required cookie
            self._tags.append((Tag.LAZY_LOAD, tag_type))
            if consent != CONSENT_TRUE:
                self.consent[tag_type] = CONSENT_TRUE

        else:
            if tag_config.get("value") == SETTING_INITIAL:
                if consent == CONSENT_UNSET:
                    # Include initial lazy tags
                    # Include initial instant tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))
                elif consent == CONSENT_TRUE:
                    # Include initial lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

            elif tag_config.get("value") == SETTING_CONTINUE:
                if consent == CONSENT_UNSET:
                    self.consent[tag_type] = CONSENT_TRUE
                elif consent == CONSENT_TRUE:
                    # Include generic lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

            else:
                if consent == CONSENT_TRUE:
                    # Include generic lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

    def should_include(self, tag_type, tag_config):
        consent = self.consent_state.get(tag_type, CONSENT_UNSET)

        if tag_config.get("value") == SETTING_REQUIRED:
            return True
        elif tag_config.get("value") == SETTING_INITIAL:
            if consent == CONSENT_UNSET or consent == CONSENT_TRUE:
                return True
        else:
            if consent == CONSENT_TRUE:
                return True

    @property
    def queryset(self):
        queryset = Q()
        for tag_type in self._tags:
            queryset.add(Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1]), Q.OR)
        return queryset

    @property
    def tags(self):
        if self._tags:
            return Tag.objects.auto_load().filter(self.queryset)
        else:
            return Tag.objects.none()

    @property
    def result(self):
        result = [
            {"object": tag, "element": tag.get_doc(self._request, self._context)}
            for tag in self.tags
        ]

        for trigger in Trigger.objects.active():
            match = trigger.match(self._request)
            if match is not None:
                for tag in trigger.tags.filter(self.queryset):
                    result.append(
                        {
                            "object": tag,
                            "element": tag.get_doc(
                                self._request, {**self._context, **match.groupdict()}
                            ),
                        }
                    )

        return result

    @property
    def cookie_state(self):
        return {
            tag_type: self.consent.get(tag_type, CONSENT_FALSE) != CONSENT_FALSE
            for tag_type in Tag.get_types()
        }
