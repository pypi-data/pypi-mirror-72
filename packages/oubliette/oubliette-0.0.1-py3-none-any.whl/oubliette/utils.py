import inspect


def is_sub(_class, obj):
    """Is this class OR instance  derived from a class,

    We often pass around class objects and instance in the same argument slot.
    Some times this doesn't matter, but some times is does.
    This will allow us to check if a class or instance is a child of a certain class.

    Args:
        _class (class): The class to check the lineage of.
        obj (object): The class/instance to inspect.

    Returns:
        bool: Is this object derived from the given class?
    """
    if inspect.isclass(obj):
        return issubclass(obj, _class)
    return isinstance(obj, _class)


class StrNameMetaclass(type):
    """Causes a class to display it's name on print"""

    def __repr__(cls):
        if getattr(cls, "name", None):
            return str(cls.name)
        return str(cls.__name__)
