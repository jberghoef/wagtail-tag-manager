from django.forms import widgets

from wagtail_tag_manager.decorators import get_variables


class VariableSelect(widgets.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = [
            (var.key, "%s - %s" % (var.name, var.description))
            for var in get_variables()
        ]


class Codearea(widgets.Textarea):
    template_name = "admin/widgets/codearea.html"

    class Media:
        css = {"all": ("wagtail_tag_manager/codearea.bundle.css",)}
        js = ("wagtail_tag_manager/codearea.bundle.js",)


class HorizontalCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    class Media:
        css = {"all": ("wagtail_tag_manager/checkbox_select_multiple.bundle.css",)}
