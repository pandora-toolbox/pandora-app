from io import StringIO
from typing import Union

from ruamel import yaml

from ..stypes import String


class Serializable:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class GenericObject:
    @staticmethod
    def load(dictionary: dict):
        from munch import DefaultMunch
        return DefaultMunch.fromDict(dictionary)


class YAML:
    __parser = yaml.YAML(typ="safe")

    @staticmethod
    def object(target_class):
        """
        Register a Python Object as YAML object to be (de)serialized.
        """
        from functools import wraps

        @wraps(target_class)
        def class_wrapper():
            YAML.__parser.register_class(target_class)

            return target_class

        return class_wrapper()

    @staticmethod
    def dump(obj: any = None, target: Union[str, StringIO] = None):
        """
        Serialize an object to a target that can be a file path or a StringIO stream.
        """
        from src.main.commons.integrations import OS

        if obj is None:
            raise ValueError("Error while trying to serialize object to file: Object is 'None'.")
        elif type(target) == StringIO or OS.Path.exists(target):
            # TODO: Improve that logic since ruamel.yaml dump Python Objects with the `!<ClassName>` keyword.
            #   The workaround is to pass the object dictionary to be dumped.
            YAML.__parser.dump(obj.__dict__, target)

    @staticmethod
    def load(path: str = None, target_class=None):
        """
        Deserialize a configuration file to an object.

        :param path: configuration file path.
        :param target_class: optional target class to contain the information.
                             The class should extend Serializable class and
                             should contain the same attributes as the provided file.
        :return: a class containing all the values defined on the file.
        """
        from src.main.commons.integrations import OS

        def get_user_attributes(cls):
            import inspect

            boring = dir(type('dummy', (object,), {}))
            return [item
                    for item in inspect.getmembers(cls)
                    if item[0] not in boring]

        if OS.Path.exists(path):
            with open(path, 'r') as file:
                parsed_dict = YAML.__parser.load(OS.Environment.expand_vars(file))

                if parsed_dict is not None:
                    if target_class is None:
                        return GenericObject.load(parsed_dict)
                    elif issubclass(target_class, Serializable):
                        import inspect

                        # inspect target_class attributes
                        members: list = [member[0] for member in inspect.getmembers(target_class)if not str(member[0]).startswith("_") ]

                        # for each, get the attribute class (should extend Serializable)
                        for member in members:
                            clsattr = getattr(target_class, member)

                            if inspect.isclass(clsattr) and issubclass(clsattr, Serializable):
                                # load object into and override the value with the parsed one
                                parsed_dict[member] = clsattr(**parsed_dict[member])

                        return target_class(**parsed_dict)
                    else:
                        raise ValueError(
                            "Error while trying to deserialize YAML File: target class is not Serializable.")
                else:
                    return None
        else:
            raise ValueError("Error while trying to deserialize file into YAML: File path is not valid.")

    @staticmethod
    def load_str(string: str = None, target_class=None):
        """
        Deserialize a YAML String to an object.

        :param string: YAML string
        :param target_class: optional target class to contain the information.
                             The class should extend Serializable class and
                             should contain the same attributes as the provided file.
        :return: a class containing all the values defined on the file.
        """
        from src.main.commons.integrations import OS

        if String.not_empty(string):
            parsed_dict = YAML.__parser.load(string)

            if parsed_dict is not None:
                if target_class is None:
                    return GenericObject.load(parsed_dict)
                elif issubclass(target_class, Serializable):
                    return target_class(**parsed_dict)
                else:
                    raise ValueError("Error while trying to deserialize YAML String: target class is not Serializable.")
            else:
                return None
        else:
            raise ValueError("Error while trying to deserialize YAML String: String is not valid.")


class JSON:
    @staticmethod
    def dump():
        pass

    @staticmethod
    def load():
        pass
