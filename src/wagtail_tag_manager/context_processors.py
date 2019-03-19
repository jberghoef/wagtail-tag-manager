from wagtail_tag_manager.strategy import TagStrategy


def consent_state(request):
    strategy = TagStrategy(request=request)
    return {"wtm_consent_state": getattr(strategy, "cookie_state", {})}
