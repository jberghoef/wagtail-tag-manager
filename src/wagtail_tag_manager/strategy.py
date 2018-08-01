from wagtail_tag_manager.models import Tag, TagTypeSettings


def define_tags(request):
    cookies = request.COOKIES
    config = TagTypeSettings.all()

    tag_types = []
    set_cookies = []

    for tag_type, tag_config in config.items():
        cookie_name = Tag.get_cookie_name(tag_type)
        cookie = cookies.get(cookie_name, None)

        if tag_config.get('required', False):
            if not cookie:
                tag_types.append((Tag.INSTANT_LOAD, tag_type))
                set_cookies.append(tag_type)
            tag_types.append((Tag.LAZY_LOAD, tag_type))
        else:
            if tag_config.get('initial', False):
                if not cookie:
                    tag_types.append((Tag.INSTANT_LOAD, tag_type))
                    tag_types.append((Tag.LAZY_LOAD, tag_type))
                elif cookie == 'true':
                    tag_types.append((Tag.LAZY_LOAD, tag_type))
            elif cookie == 'true':
                tag_types.append((Tag.LAZY_LOAD, tag_type))

    return tag_types, set_cookies
