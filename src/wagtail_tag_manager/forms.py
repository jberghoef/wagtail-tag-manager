from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail_tag_manager.models import TagTypeSettings


class ConsentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in TagTypeSettings.all().items():
            self.fields[key] = forms.BooleanField(
                label=_(key.title()),
                required=value.get('required'),
                disabled=value.get('required'),
                initial=value.get('initial') is True)
