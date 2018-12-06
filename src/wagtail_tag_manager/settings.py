from django.conf import settings


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
