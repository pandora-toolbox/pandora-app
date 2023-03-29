from ..stypes import String


class Serializable:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class GenericObject:
    @staticmethod
    def serialize():
        # save to a file
        pass

    @staticmethod
    def deserialize(dictionary: dict):
        from munch import DefaultMunch
        return DefaultMunch.fromDict(dictionary)


class YAML:
    @staticmethod
    def serialize():
        pass

    @staticmethod
    def deserialize(path: str = None, target_class=None):
        """
        Load a configuration file to an object.

        :param path: configuration file path.
        :param target_class: optional target class to contain the information.
                             The class should extend Serializable class and
                             should contain the same attributes as the provided file.
        :return: a class containing all the values defined on the file.
        """
        if String.is_empty(path):
            raise ValueError("YAML file path is not valid.")

        # TODO: validate the path structure

        with open(path, 'r') as file:
            import yaml
            import os

            parsed_dict = yaml.safe_load(os.path.expandvars(file.read()))

            if parsed_dict is not None:
                if target_class is None:
                    return GenericObject.deserialize(parsed_dict)
                elif issubclass(target_class, Serializable):
                    return target_class(**parsed_dict)
            else:
                return None

    @staticmethod
    def to_json():
        pass


class JSON:
    @staticmethod
    def serialize():
        pass

    @staticmethod
    def deserialize():
        pass

    @staticmethod
    def generic_serialize():
        pass

    @staticmethod
    def to_yaml():
        pass
