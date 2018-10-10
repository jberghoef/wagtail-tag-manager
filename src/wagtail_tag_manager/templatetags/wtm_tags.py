from django import template
from django.conf import settings
from django.urls import reverse

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import get_cookie_state
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import TagStrategy

register = template.Library()


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/instant_tags.html", takes_context=True
)
def wtm_instant_tags(context):
    context["tags"] = []
    request = context.get("request", None)

    if request is not None:
        strategy = TagStrategy(request)

        contents = []
        for item in strategy.result:
            contents += item.get("content", [])

        context["tags"] = [tag.prettify() for tag in contents]

    return context


@register.inclusion_tag("wagtail_tag_manager/templatetags/lazy_manager.html")
def wtm_lazy_manager():
    return {
        "config": {"state_url": reverse("wtm:state"), "lazy_url": reverse("wtm:lazy")}
    }


@register.inclusion_tag("wagtail_tag_manager/templatetags/cookie_bar.html")
def wtm_cookie_bar():
    return {"manage_view": getattr(settings, "WTM_MANAGE_VIEW", True)}


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/manage_form.html", takes_context=True
)
def wtm_manage_form(context):
    request = context.get("request")
    return {"form": ConsentForm(initial=get_cookie_state(request))}


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/status_table.html", takes_context=True
)
def wtm_status_table(context):
    context["tags"] = {}
    for tag_type in Tag.get_types():
        context["tags"][tag_type] = Tag.objects.filter(tag_type=tag_type)
    return context
