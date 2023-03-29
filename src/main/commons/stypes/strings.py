from typing import Type, Any, Optional


class String:
    EMPTY: Type[str] = ""

    @staticmethod
    def is_empty(value) -> bool:
        return String.equals(value, String.EMPTY)

    @staticmethod
    def not_empty(value):
        return not String.is_empty(value)

    @staticmethod
    def equals(first_value: Any, second_value: Any):
        def get_comparable(string: Any) -> Optional[str]:
            """ Get the String Comparable value of an object """
            comparable: Any
            if string is not None and String.EMPTY != string:
                if type(string) == str:
                    comparable = string
                else:
                    comparable = str(string)
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
