from wagtail_tag_manager.options import CustomVariable

_variables: dict = {}


def register_variable(cls=None):
    if not issubclass(cls, CustomVariable):
        raise ValueError("Class must subclass CustomVariable.")

    if cls is None:  # pragma: no cover

        def decorator(cls):
            register_variable(cls)
            return cls

        return decorator

    _variables[cls.key] = cls


def get_variables():
    """ Return the variables function sorted by their order. """
    return [cls() for key, cls in _variables.items()]
