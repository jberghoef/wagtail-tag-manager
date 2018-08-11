import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.models import Tag, TagTypeSettings
from wagtail_tag_manager.strategy import TagStrategy
from wagtail_tag_manager.utils import get_cookie_state

register = template.Library()


@register.inclusion_tag(
    'wagtail_tag_manager/templatetags/instant_tags.html', takes_context=True)
def wtm_instant_tags(context):
    context['tags'] = []
    request = context.get('request', None)

    if request is not None:
        strategy = TagStrategy(request)
        tag_context = Tag.create_context(request)

        content = []
        for tag in Tag.objects.active().filter(strategy.queryset):
            content += tag.get_contents(request, tag_context)

        context['tags'] = [mark_safe(tag.prettify()) for tag in content]

    return context


@register.inclusion_tag('wagtail_tag_manager/templatetags/lazy_manager.html')
def wtm_lazy_manager():
    return {
        'config': TagTypeSettings.all(),
    }


@register.inclusion_tag('wagtail_tag_manager/templatetags/cookie_bar.html')
def wtm_cookie_bar():
    return {
        'manage_view': getattr(settings, 'WTM_MANAGE_VIEW', True),
    }


@register.inclusion_tag(
    'wagtail_tag_manager/templatetags/manage_form.html', takes_context=True)
def wtm_manage_form(context):
    request = context.get('request')
    return {
        'form': ConsentForm(initial=get_cookie_state(request)),
    }


@register.inclusion_tag(
    'wagtail_tag_manager/templatetags/status_table.html', takes_context=True)
def wtm_status_table(context):
    context['tags'] = {}
    for tag_type in Tag.get_types():
        context['tags'][tag_type] = Tag.objects.filter(tag_type=tag_type)
    return context
