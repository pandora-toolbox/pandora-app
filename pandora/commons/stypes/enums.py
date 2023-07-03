from enum import Enum


class SerializableEnum(Enum):
    @classmethod
    def get_from(cls, value):
        if value is not None:
            for _enum in cls:
                if _enum.value == value:
                    return _enum