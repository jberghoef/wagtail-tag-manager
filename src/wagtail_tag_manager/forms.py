from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail_tag_manager.models import TagTypeSettings


class ConsentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tag_type, config in TagTypeSettings.all().items():
            initial = config == "initial" or config == "required"
            if "initial" in kwargs:
                initial = kwargs.get("initial")[tag_type]

            self.fields[tag_type] = forms.BooleanField(
                label=_(tag_type.title()),
                required=config == "required",
                disabled=config == "required",
                initial=initial,
            )
