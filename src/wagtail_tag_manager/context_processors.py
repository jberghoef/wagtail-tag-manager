from wagtail_tag_manager.strategy import TagStrategy


def cookie_state(request):
    strategy = TagStrategy(request=request)
    return {"wtm_cookie_state": getattr(strategy, "cookie_state", {})}
