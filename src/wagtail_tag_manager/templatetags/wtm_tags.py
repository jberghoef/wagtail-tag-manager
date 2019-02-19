from bs4 import BeautifulSoup
from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.models import Tag, CookieDeclaration
from wagtail_tag_manager.settings import CookieBarSettings, TagTypeSettings
from wagtail_tag_manager.strategy import TagStrategy

register = template.Library()


class IncludeNode(template.Node):
    def __init__(self, nodelist, tag_type, src):
        if not tag_type:
            raise template.TemplateSyntaxError(_("Provide a `tag_type` argument."))

        self.nodelist = nodelist
        self.tag_type = tag_type.replace('"', "")
        self.src = src.replace('"', "")

    def render(self, context):
        request = context.get("request", None)
        if request:
            tag_config = TagTypeSettings().get(self.tag_type)

            if TagStrategy(request=request).should_include(self.tag_type, tag_config):
                ctx = Tag.create_context(request=request, context=context)

                if self.src:
                    if self.src.endswith(".html"):
                        return render_to_string(self.src, ctx)

                    elif self.src.endswith(".css"):
                        tag = BeautifulSoup("", "html.parser").new_tag("link")
                        tag["rel"] = "stylesheet"
                        tag["type"] = "text/css"
                        tag["href"] = static(self.src)

                    elif self.src.endswith(".js"):
                        tag = BeautifulSoup("", "html.parser").new_tag("script")
                        tag["type"] = "text/javascript"
                        tag["src"] = static(self.src)

                    return mark_safe(tag.decode())

                output = self.nodelist.render(ctx)
                return output

        return ""


@register.tag
def wtm_include(parser, token):
    try:
        args = token.contents.split(None)[1:]

        nodelist = None

        if len(args) == 1:
            nodelist = parser.parse(("wtm_endinclude",))
            parser.delete_first_token()
            args.append("")

        return IncludeNode(nodelist, *args)

    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
        )


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
def wtm_cookie_bar(context):
    request = context.get("request", None)
    if request:
        cookie_state = TagStrategy(request).cookie_state

        cookie_bar_settings = {}
        if getattr(request, "site", None):
            cookie_bar_settings = CookieBarSettings.for_site(request.site)

        manage_view = getattr(settings, "WTM_MANAGE_VIEW", True)
        if manage_view and hasattr(request, "resolver_match"):
            manage_view = (
                getattr(request.resolver_match, "view_name", "") != "wtm:manage"
            )

        return {
            "manage_view": manage_view,
            "form": ConsentForm(initial=cookie_state),
            "settings": cookie_bar_settings,
            "declarations": CookieDeclaration.objects.all().sorted(),
        }

    return ""


@register.inclusion_tag(
    "wagtail_tag_manager/templatetags/manage_form.html", takes_context=True
)
def wtm_manage_form(context):
    request = context.get("request")
    if request:
        cookie_state = TagStrategy(request).cookie_state
        return {"form": ConsentForm(initial=cookie_state)}
    return ""


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
