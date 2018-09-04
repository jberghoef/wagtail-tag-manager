from django.db.models import Q

from wagtail_tag_manager.models import Tag, TagTypeSettings


class TagStrategy(object):
    def __init__(self, request, consent=None):
        self.cookies = request.COOKIES
        self.config = TagTypeSettings.all()

        self.include_tags = []
        self.include_cookies = {}

        self.define_strategy(request=request, consent=consent)
        self.build_queryset()

    # https://gist.github.com/jberghoef/9ffa2b738cbb0aab624ff091dc6fe9a7
    def define_strategy(self, request, consent):
        for tag_type, tag_config in self.config.items():
            handler = getattr(self, request.method.lower(), None)
            if handler:
                handler(request, consent, tag_type, tag_config)

    def get(self, request, consent, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self.cookies.get(cookie_name, None)

        if tag_config == 'required':
            # Include required instant tags
            # Include required cookie
            self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
            self.include_cookies[cookie_name] = 'true'
        elif tag_config == 'initial':
            if cookie == 'true':
                # Include initial instant tags
                self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
        else:
            if cookie == 'true':
                # Include generic instant tags
                self.include_tags.append((Tag.INSTANT_LOAD, tag_type))

    def post(self, request, consent, tag_type, tag_config):
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = self.cookies.get(cookie_name, None)

        if tag_config == 'required':
            # Include required lazy tags
            # Include required cookie
            if consent is None:
                self.include_tags.append((Tag.LAZY_LOAD, tag_type))
            if cookie != 'true':
                self.include_cookies[cookie_name] = 'true'

        elif consent is None:
            if tag_config == 'initial':
                if cookie == 'unset':
                    # Include initial lazy tags
                    # Include initial instant tags
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))
                    self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
                elif cookie == 'true':
                    # Include initial lazy tags
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))
            else:
                if cookie == 'true':
                    # Include generic lazy tags
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))

        elif consent is True:
            if tag_config == 'initial':
                if cookie == 'false':
                    # Include initial lazy tags
                    # Include initial instant tags
                    # Include initial cookie
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))
                    self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
                self.include_cookies[cookie_name] = 'true'
            else:
                if cookie == 'true':
                    pass
                else:
                    # Include generic lazy tags
                    # Include generic instant tags
                    # Include generic cookie
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))
                    self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
                    self.include_cookies[cookie_name] = 'true'

        elif consent is False:
            self.include_cookies[cookie_name] = 'false'

    def build_queryset(self):
        self.queryset = Q()
        for tag_type in self.include_tags:
            self.queryset.add(
                Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1]), Q.OR)
