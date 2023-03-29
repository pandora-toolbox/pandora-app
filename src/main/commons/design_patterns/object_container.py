from typing import Dict

from ..stypes import String
from .singleton import Singleton


class ObjectContainer(metaclass=Singleton):
    def __init__(self):
        self.objects: Dict[str, object] = {}

    @staticmethod
    def obj_signature(obj: object):
        """Provides the module and the class name of an object"""
        if object is not None:
            import inspect

            module_name: str = inspect.getmodule(obj).__name__
            obj_name: str = obj.__name__ if isinstance(obj, type) else type(obj).__name__

            return f"{module_name}.{obj_name}"

    def add(self, obj: object, key: str = None) -> None:
        """
        Add an object to the ObjectContainer.

        :param key: the key to access the object. If nothing is provided, the key will be the object signature.
        :param obj:  the object that should be placed inside the container. Should not be None.
        """
        error_msg: str = f"Error while trying to add object to {str(self.__class__)}: "

        if obj is None and String.not_empty(key):
            raise ValueError(error_msg + f"Object with key '{key}' is None.")
        if obj is None and String.is_empty(key):
            raise ValueError(error_msg + f"Object is None.")

        if String.is_empty(key):
            import inspect

            key = ObjectContainer.obj_signature(obj)

        self.objects[key] = obj

    def get(self, key: str):
        """Get an element from the Object Container"""
        element: object = None

        if String.not_empty(key):
            try:
                element = self.objects[key]
            except KeyError:
                pass

        return element

    def clear(self):
        self.objects: Dict[str, object] = {}

    def __str__(self):
        return str(self.__dict__)


def inject(f):
    """
    Allow a Dependency Injection to methods based on:
    * parameter name (should be equals to an object key in the ObjectContainer)
    * object signature (only valid for objects created from a class)
    The injected object is the same object instead of a copy.
    """
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwds):
        def get_func_fields() -> dict:
            """Get the argument definition of the function that needs to have values injected"""
            from inspect import FullArgSpec, getfullargspec
            from collections import OrderedDict
            import itertools

            f_arg_spec: FullArgSpec = getfullargspec(f)

            spec: OrderedDict = OrderedDict()
            # `itertools.zip_longest` is used because it is possible to have more fields declared (`f_arg_spec.args`)
            # than values for them (`args`)
            for arg_name, arg_value in itertools.zip_longest(f_arg_spec.args, args):
                arg_type = None

                if arg_value is None:
                    try:
                        arg_type = f_arg_spec.annotations[arg_name]
                    except KeyError:
                        pass

                spec[arg_name] = {
                    "type": arg_type,
                    "value": arg_value
                }

            return spec

        fields = get_func_fields()  # All function fields definition
        container: ObjectContainer = ObjectContainer()  # Should be a Singleton :)
        new_args: tuple = tuple()

        # Inject the values based on the field name or in the object signature
        for name, field in zip(fields.keys(), fields.values()):
            if name != "self":
                # Check the field value for the first time
                if field["value"] is None:
                    # try to inject value by seeking for something with the same key as the field name
                    field["value"] = container.get(name)

                    # Check if an object was injected
                    if field["value"] is None:
                        # Try to inject an object based on the signature
                        field["value"] = container.get(ObjectContainer.obj_signature(field["type"]))

                    # Last check if the field was properly populated. If not, raise an error
                    if field["value"] is None:
                        raise RuntimeError(f"There is no object available in ObjectContainer to inject.")

            # Add the field value in an ordered way to be used as a function argument
            new_args += (field["value"],)

        return f(*new_args, **kwds)
    return wrapper
