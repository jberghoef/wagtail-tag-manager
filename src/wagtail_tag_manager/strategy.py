from django.db.models import Q

from wagtail_tag_manager.models import Tag, Trigger, TagTypeSettings
from wagtail_tag_manager.settings import (
    SETTING_INITIAL,
    SETTING_CONTINUE,
    SETTING_REQUIRED,
)

COOKIE_TRUE = "true"
COOKIE_FALSE = "false"
COOKIE_UNSET = "unset"


class TagStrategy(object):
    def __init__(self, request):
        self._request = request
        self._context = Tag.create_context(request)

        self._cookies = getattr(request, "COOKIES", {})
        self._config = TagTypeSettings.all()
        self._tags = []
        self.cookies = {}

        if request:
            self.define_strategy()

    # https://gist.github.com/jberghoef/9ffa2b738cbb0aab624ff091dc6fe9a7
    def define_strategy(self):
        for tag_type, tag_config in self._config.items():
            handler = getattr(self, self._request.method.lower(), None)
            if handler:
                handler(tag_type, tag_config)

    def get(self, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self._cookies.get(cookie_name, None)

        if tag_config.get("value") == SETTING_REQUIRED:
            # Include required instant tags
            # Include required cookie
            self._tags.append((Tag.INSTANT_LOAD, tag_type))
            self.cookies[cookie_name] = COOKIE_TRUE

        elif tag_config.get("value") == SETTING_INITIAL:
            if not cookie or cookie == COOKIE_UNSET:
                # Include initial cookie
                self.cookies[cookie_name] = COOKIE_UNSET
            elif cookie == COOKIE_TRUE:
                # Include initial instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = COOKIE_TRUE

        elif tag_config.get("value") == SETTING_CONTINUE:
            if not cookie or cookie == COOKIE_UNSET:
                # Include initial cookie
                self.cookies[cookie_name] = COOKIE_UNSET
            elif cookie == COOKIE_TRUE:
                # Include initial instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = COOKIE_TRUE

        else:
            if cookie == COOKIE_TRUE:
                # Include generic instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = COOKIE_TRUE

    def post(self, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self._cookies.get(cookie_name, None)

        if tag_config.get("value") == SETTING_REQUIRED:
            # Include required lazy tags
            # Include required cookie
            self._tags.append((Tag.LAZY_LOAD, tag_type))
            if cookie != COOKIE_TRUE:
                self.cookies[cookie_name] = COOKIE_TRUE

        else:
            if tag_config.get("value") == SETTING_INITIAL:
                if cookie == COOKIE_UNSET:
                    # Include initial lazy tags
                    # Include initial instant tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))
                elif cookie == COOKIE_TRUE:
                    # Include initial lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

            elif tag_config.get("value") == SETTING_CONTINUE:
                if cookie == COOKIE_UNSET:
                    self.cookies[cookie_name] = COOKIE_TRUE
                elif cookie == COOKIE_TRUE:
                    # Include generic lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

            else:
                if cookie == COOKIE_TRUE:
                    # Include generic lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

    def should_include(self, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self._cookies.get(cookie_name, None)

        if tag_config.get("value") == SETTING_REQUIRED:
            return True
        elif tag_config.get("value") == SETTING_INITIAL:
            if not cookie or cookie == COOKIE_UNSET or cookie == COOKIE_TRUE:
                return True
        else:
            if cookie == COOKIE_TRUE:
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
            tag_type: self.cookies.get(Tag.get_cookie_name(tag_type), COOKIE_FALSE)
            != COOKIE_FALSE
            for tag_type in Tag.get_types()
        }
