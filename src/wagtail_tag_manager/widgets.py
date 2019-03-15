from django.forms.widgets import CheckboxSelectMultiple


class StackedCheckboxSelectMultiple(CheckboxSelectMultiple):
    def build_attrs(self, base_attrs, extra_attrs=None):
        return {
            **base_attrs,
            "class": "stacked_checkbox_select_multiple",
            **(extra_attrs or {}),
        }

    class Media:
        css = {"all": ("checkbox_select_multiple.bundle.css",)}
        js = "checkbox_select_multiple.bundle.js"
