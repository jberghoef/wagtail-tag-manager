from django.utils.translation import ugettext_lazy as _


class CustomVariable(object):
    name = ""
    description = ""
    key = ""
    group = _("Various")
    lazy_only = False

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        for field in ["name", "description", "key"]:
            if not getattr(self, field, None):
                raise ValueError(
                    f"A CustomVariable class has to provide a '{field}' value."
                )

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "group": self.group,
            "lazy_only": self.lazy_only,
            "variable_type": "custom",
            "value": "not available",
        }

    def get_value(self, request):
        return ""
