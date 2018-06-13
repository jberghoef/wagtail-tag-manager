from django import template

from ..forms import ConsentForm
from ..models import Tag
from ..utils import get_cookie_state

register = template.Library()


@register.inclusion_tag('templatetags/manage_form.html', takes_context=True)
def wtm_manage_form(context):
    request = context.get('request')
    return {
        'form': ConsentForm(initial=get_cookie_state(request)),
    }


@register.inclusion_tag('templatetags/status_table.html', takes_context=True)
def wtm_status_table(context):
    request = context.get('request')
    return {
        **get_cookie_state(request),
        'tags': Tag.objects.active(),
    }
