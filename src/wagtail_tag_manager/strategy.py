from django.db.models import Q

from wagtail_tag_manager.models import Tag, TagTypeSettings


class TagStrategy(object):
    def __init__(self, request, consent=False):
        self.cookies = request.COOKIES
        self.config = TagTypeSettings.all()

        self.include_tags = []
        self.include_cookies = []

        self.define_strategy(request=request, consent=consent)
        self.build_queryset()

    # https://gist.github.com/jberghoef/9ffa2b738cbb0aab624ff091dc6fe9a7
    def define_strategy(self, request, consent=False):
        for tag_type, tag_config in self.config.items():
            cookie_name = Tag.get_cookie_name(tag_type)
            cookie = self.cookies.get(cookie_name, None)

            if request.method == 'GET':  # Middleware logic
                if tag_config.get('required', False):
                    # Include required instant tags
                    self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
                    if cookie != 'true':
                        # Include required cookie
                        self.include_cookies.append(cookie_name)
                elif tag_config.get('initial', False):
                    if cookie != 'false':
                        # Include initial instant tags
                        self.include_tags.append((Tag.INSTANT_LOAD, tag_type))
                else:
                    if cookie == 'true':
                        # Include generic instant tags
                        self.include_tags.append((Tag.INSTANT_LOAD, tag_type))

            elif request.method == 'POST':  # Endpoint logic
                if tag_config.get('required', False):
                    # Include required lazy tags
                    self.include_tags.append((Tag.LAZY_LOAD, tag_type))
                    if cookie != 'true':
                        # Include required cookie
                        self.include_cookies.append(cookie_name)

                elif consent is False:
                    if tag_config.get('initial', False):
                        if cookie != 'false':
                            # Include initial lazy tags
                            self.include_tags.append((Tag.LAZY_LOAD, tag_type))
                    else:
                        if cookie == 'true':
                            # Include generic lazy tags
                            self.include_tags.append((Tag.LAZY_LOAD, tag_type))

                elif consent is True:
                    if tag_config.get('initial', False):
                        if cookie == 'false':
                            # Include initial lazy tags
                            # Include initial instant tags
                            # Include initial cookie
                            self.include_tags.append(
                                (Tag.LAZY_LOAD, tag_type),
                                (Tag.INSTANT_LOAD, tag_type))
                            self.include_cookies.append(cookie_name)
                    else:
                        if cookie == 'true':
                            pass
                        else:
                            # Include generic lazy tags
                            # Include generic instant tags
                            # Include generic cookie
                            self.include_tags.append(
                                (Tag.LAZY_LOAD, tag_type),
                                (Tag.INSTANT_LOAD, tag_type))
                            self.include_cookies.append(cookie_name)

    def build_queryset(self):
        self.queryset = Q()
        for tag_type in self.include_tags:
            self.queryset.add(
                Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1]), Q.OR)
