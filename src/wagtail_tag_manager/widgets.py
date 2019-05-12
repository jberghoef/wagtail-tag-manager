from django.forms import widgets

from wagtail_tag_manager.decorators import get_variables


class VariableSelect(widgets.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = [
            (var.key, "%s - %s" % (var.name, var.description))
            for var in get_variables()
        ]
