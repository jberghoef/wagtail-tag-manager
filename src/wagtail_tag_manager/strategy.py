from django.db.models import Q

from wagtail_tag_manager.models import Tag, Trigger, TagTypeSettings


class TagStrategy(object):
    def __init__(self, request, consent=None):
        self._request = request
        self._consent = consent
        self._context = Tag.create_context(request)

        self._cookies = request.COOKIES
        self._config = TagTypeSettings.all()
        self._tags = []

        self.cookies = {}

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

        if tag_config == "required":
            # Include required instant tags
            # Include required cookie
            self._tags.append((Tag.INSTANT_LOAD, tag_type))
            self.cookies[cookie_name] = "true"
        elif tag_config == "initial":
            if not cookie or cookie == "unset":
                # Include initial cookie
                self.cookies[cookie_name] = "unset"
            elif cookie == "true":
                # Include initial instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = "true"
        else:
            if cookie == "true":
                # Include generic instant tags
                self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = "true"

    def post(self, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self._cookies.get(cookie_name, None)

        if tag_config == "required":
            # Include required lazy tags
            # Include required cookie
            if self._consent is None:
                self._tags.append((Tag.LAZY_LOAD, tag_type))
            if cookie != "true":
                self.cookies[cookie_name] = "true"

        elif self._consent is None:
            if tag_config == "initial":
                if cookie == "unset":
                    # Include initial lazy tags
                    # Include initial instant tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))
                elif cookie == "true":
                    # Include initial lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
            else:
                if cookie == "true":
                    # Include generic lazy tags
                    self._tags.append((Tag.LAZY_LOAD, tag_type))

        elif self._consent is True:
            if tag_config == "initial":
                if cookie == "false":
                    # Include initial lazy tags
                    # Include initial instant tags
                    # Include initial cookie
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))
                self.cookies[cookie_name] = "true"
            else:
                if cookie == "true":
                    pass
                else:
                    # Include generic lazy tags
                    # Include generic instant tags
                    # Include generic cookie
                    self._tags.append((Tag.LAZY_LOAD, tag_type))
                    self._tags.append((Tag.INSTANT_LOAD, tag_type))
                    self.cookies[cookie_name] = "true"

        elif self._consent is False:
            self.cookies[cookie_name] = "false"

    @property
    def queryset(self):
        queryset = Q()
        for tag_type in self._tags:
            queryset.add(Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1]), Q.OR)
        return queryset

    @property
    def tags(self):
        if self._tags:
            return Tag.objects.active().filter(self.queryset)
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
            tag_type: self.cookies.get(Tag.get_cookie_name(tag_type), "false")
            != "false"
            for tag_type in Tag.get_types()
        }
