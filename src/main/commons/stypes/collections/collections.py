from typing import Optional, List, Tuple

from src.main.commons.stypes.collections.gcollection import GenericCollection


class Collection:
    @staticmethod
    def is_empty(collection=None):
        return collection is None or (collection is not None and len(collection) == 0)

    @staticmethod
    def not_empty(collection=None):
        return not Collection.is_empty(collection)

    @staticmethod
    def __get_from_dict(collection: dict, key):
        if Collection.not_empty(collection):
            try:
                return collection[key]
            except KeyError:
                return None

    @staticmethod
    def is_present(collection=None, obj: object = None):
        return True if Collection.get_from(collection, obj) is not None else False

    @staticmethod
    def __get_from_list(collection=None, obj: object = None):
        if collection is not None:
            if type(collection) is list:
                try:
                    target_list: list = collection
                    index: int = target_list.index(obj)
                    return target_list[index]
                except ValueError:
                    return None

    @staticmethod
    def get_from(collection=None, key=None) -> Optional[object]:
        if type(collection) is list:
            return Collection.__get_from_list(collection, key)

        if type(collection) is dict:
            return Collection.__get_from_dict(collection, key)

        # Fallback for get the object dictionary
        return Collection.__get_from_dict(collection.__dict__, key)

    @staticmethod
    def dict_to_tuple_list(src_dict: dict) -> List[Tuple[str, object]]:
        if Collection.not_empty(src_dict):
            if not isinstance(src_dict, dict):
                src_dict = src_dict.__dict__

            return [(key, src_dict[key]) for key in src_dict.keys()]
        else:
            return []

    @staticmethod
    def to_dict(collection=None):
        if type(collection) is list:
            __dict: dict = {}

            for item in collection:
                __dict[item] = item


from typing import Any, Dict, List, Tuple
import threading


class SafeAccess:
    @staticmethod
    def get_item(obj: Any, key: Any) -> Any:
        """
        Safely retrieves an item from a collection, with thread-safe access for dictionaries.

        Args:
            obj: The collection to retrieve the item from.
            key: The key or index of the item to retrieve.

        Returns:
            The item at the specified key or index, or None if it does not exist.
        """
        if isinstance(obj, dict):
            with threading.Lock():
                return obj.get(key)
        elif isinstance(obj, (list, tuple)):
            with threading.Lock():
                if 0 <= key < len(obj):
                    return obj[key]
        elif isinstance(obj, GenericCollection):
            return obj.get(key)
        else:
            raise TypeError(f"{type(obj).__name__} is not a supported type for safe access")

    @staticmethod
    def is_present(obj: Any, key: Any) -> bool:
        """
        Checks if an item is present in a collection, with thread-safe access for dictionaries.

        Args:
            obj: The collection to check for the presence of the item.
            key: The key or index of the item to check.

        Returns:
            True if the item is present in the collection, False otherwise.
        """
        try:
            value = SafeAccess.get_item(obj, key)
            return value is not None
        except:
            return False

    @staticmethod
    def not_present(obj: Any, key: Any) -> bool:
        """
        Checks if an item is not present in a collection, with thread-safe access for dictionaries.

        Args:
            obj: The collection to check for the absence of the item.
            key: The key or index of the item to check.

        Returns:
            True if the item is not present in the collection, False otherwise.
        """
        return not SafeAccess.is_present(obj, key)

    @staticmethod
    def convert(collection: Any, target_type: type) -> Any:
        """
        Converts a collection to the specified target type, if possible.

        Args:
            collection: The collection to convert.
            target_type: The target type to convert the collection to.

        Returns:
            The converted collection, or the original collection if it cannot be converted.
        """
        if isinstance(collection, target_type):
            return collection
        elif target_type == dict:
            if isinstance(collection, (list, tuple)):
                with threading.Lock():
                    return {i: v for i, v in enumerate(collection)}
        elif target_type in (list, tuple):
            if isinstance(collection, dict):
                with threading.Lock():
                    return [v for _, v in sorted(collection.items())]
        else:
            raise TypeError(f"{target_type.__name__} is not a supported target type for conversion")
