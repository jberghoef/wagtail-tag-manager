from django import template

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.utils import get_cookie_state

register = template.Library()


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
