from django import forms
from django.utils.translation import ugettext_lazy as _


class ConsentForm(forms.Form):
    functional = forms.BooleanField(
        label=_("Functional"), required=True, disabled=True, initial=True)
    analytical = forms.BooleanField(label=_("Analytical"), required=False)
    traceable = forms.BooleanField(label=_("Traceable"), required=False)
