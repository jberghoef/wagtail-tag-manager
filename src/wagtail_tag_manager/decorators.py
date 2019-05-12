import inspect

from wagtail_tag_manager.options import CustomVariable

_variables: dict = {}


def register_variable(cls=None):
    if inspect.isclass(cls) and not issubclass(cls, CustomVariable):
        raise ValueError("Class must subclass CustomVariable.")

    if cls is None:  # pragma: no cover

        def decorator(cls):
            register_variable(cls)
            return cls

        return decorator

    _variables[cls.key] = cls


def get_variables(lazy=None):
    """ Return the variables function sorted by their order. """
    variables = []

    for key, cls in _variables.items():
        if lazy is not None and cls.lazy_only is not lazy:
            continue

        if inspect.isclass(cls):
            variables.append(cls())
        else:
            variables.append(cls)

    return variables
