class CustomVariable(object):
    name = ""
    description = ""
    key = ""

    def __init__(self, *args, **kwargs):
        for field in ["name", "description", "key"]:
            if not getattr(self, field, None):
                raise ValueError(
                    f"A CustomVariable class has to provide a '{field}' value."
                )

        super().__init__(*args, **kwargs)

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "variable_type": "custom",
            "value": "not available",
        }

    def get_value(self, request):
        return ""
