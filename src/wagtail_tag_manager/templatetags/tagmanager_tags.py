from django import template

from ..models import Tag

register = template.Library()


class AbstractNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    class Meta:
        abstract = True


@register.tag(name='tracking')
def do_tracking(parser, token):
    nodelist = parser.parse(('endtracking',))
    parser.delete_first_token()
    return TrackingNode(nodelist)


class TrackingNode(AbstractNode):
    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()
