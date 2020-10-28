from rest_framework import serializers

from wagtail_tag_manager.settings import (
    SETTING_INITIAL,
    SETTING_REQUIRED,
    TagTypeSettings,
)


class ConsentSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for tag_type, config in TagTypeSettings.all().items():
            value = config.get("value")
            initial = value == SETTING_INITIAL or value == SETTING_REQUIRED

            if SETTING_INITIAL in kwargs:
                initial = kwargs.get(SETTING_INITIAL)[tag_type]

            self.fields[tag_type] = serializers.BooleanField(
                label=config.get("verbose_name"),
                required=value == SETTING_REQUIRED,
                initial=initial,
            )
