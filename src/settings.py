from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class TagTypeSettings:
    def __init__(self):
        self.SETTINGS = {}

    @staticmethod
    def all():
        return getattr(
            settings,
            "WTM_TAG_TYPES",
            {"functional": "required", "analytical": "initial", "traceable": ""},
        )

    def get(self, tag_type):
        if not tag_type or tag_type not in self.all():
            raise ValueError(_("Provide a valid `tag_type`."))
        return self.all().get(tag_type, "")

    def include(self, value, *args, **kwargs):
        self.SETTINGS.update({k: v for k, v in self.all().items() if v == value})

        return self

    def exclude(self, value, *args, **kwargs):
        if not self.SETTINGS:
            self.SETTINGS = self.all()

        remove = []
        for k, v in self.SETTINGS.items():
            if v == value:
                remove.append(k)

        for item in remove:
            self.SETTINGS.pop(item, None)

        return self

    def result(self):
        return self.SETTINGS
