"""Implements a function which can be used as a singleton decorator."""


def singleton(classname):
    """Decorator function which restricts decorated class to be singleton.

    Args:
      classname: Reference of class whose object needs to be created.

    Returns: Instance of requested class.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """Creates (if not already created) and returns object of a class."""
        if classname not in instances:
            instances[classname] = classname(*args, **kwargs)
        return instances[classname]
    return get_instance
