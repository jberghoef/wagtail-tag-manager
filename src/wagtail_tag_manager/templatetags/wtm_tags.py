from django import template
from django.conf import settings
from django.urls import reverse

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.models import Tag, CookieDeclaration
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
        context["tags"] = [tag.get("element").decode() for tag in strategy.result]

    return context


@register.inclusion_tag("wagtail_tag_manager/templatetags/lazy_manager.html")
def wtm_lazy_manager():
    return {
        "config": {"state_url": reverse("wtm:state"), "lazy_url": reverse("wtm:lazy")}
    }


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/cookie_bar.html", takes_context=True
)
def wtm_cookie_bar(context, include_form=False):
    request = context.get("request")
    cookie_state = TagStrategy(request).cookie_state

    return {
        "manage_view": getattr(settings, "WTM_MANAGE_VIEW", True),
        "include_form": include_form,
        "form": ConsentForm(initial=cookie_state),
    }


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/manage_form.html", takes_context=True
)
def wtm_manage_form(context):
    request = context.get("request")
    cookie_state = TagStrategy(request).cookie_state

    return {"form": ConsentForm(initial=cookie_state)}


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/tag_table.html", takes_context=True
)
def wtm_tag_table(context):
    context["tags"] = Tag.objects.all().sorted()
    return context


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/declaration_table.html", takes_context=True
)
def wtm_declaration_table(context):
    context["declarations"] = CookieDeclaration.objects.all().sorted()
    return context
