from django import forms

from wagtail_tag_manager.settings import TagTypeSettings


class ConsentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for tag_type, config in TagTypeSettings.all().items():
            initial = (
                config.get("value") == "initial" or config.get("value") == "required"
            )
            if "initial" in kwargs:
                initial = kwargs.get("initial")[tag_type]

            self.fields[tag_type] = forms.BooleanField(
                label=config.get("verbose_name"),
                required=config.get("value") == "required",
                disabled=config.get("value") == "required",
                initial=initial,
            )
