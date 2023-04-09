from typing import Any, Optional


class String:
    EMPTY: str = ""

    @staticmethod
    def is_empty(value) -> bool:
        """
        Check if a value is 'None' or empty (String.EMPTY).
        If an object different from a string is passed, the target object will be parsed into a string.
        """
        return String.equals(value, String.EMPTY)

    @staticmethod
    def not_empty(value):
        """
        Check if a value is not 'None' or empty. It is the same as `not String.is_empty(value)`
        """
        return not String.is_empty(value)

    @staticmethod
    def equals(first_value: Any, second_value: Any) -> bool:
        """Check if two text values are equals."""
        def get_comparable(value: Any) -> Optional[str]:
            """ Get the String Comparable value of an object """

            comparable: Optional[str]
            if value is not None and String.EMPTY != value:
                if type(value) == str:
                    comparable = value
                else:
                    comparable = str(value)
            else:
                comparable = None

            return comparable

        first_value = get_comparable(first_value)
        second_value = get_comparable(second_value)

        return first_value == second_value

    @staticmethod
    def random(length: int):
        import random, string

        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def wrap(function):
        """Wrap a class as String. Useful for use with property decorator"""
        from functools import wraps

        @wraps(function)
        def wrapper(*args, **kwargs):
            return str(function(*args, **kwargs))

        return wrapper
