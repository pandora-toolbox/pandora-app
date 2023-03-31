from enum import Enum

from ...commons.stypes import String
from ..components import ObjectPool


class AppEnvironment(Enum):
    oid = "app.preferences.environment"

    DEV = "dev"
    PRD = "prd"

    @classmethod
    def get(cls) -> str:
        return ObjectPool().get(str(cls.oid))

    @classmethod
    def is_dev(cls):
        return String.equals(cls.DEV, cls.get())

    @classmethod
    def is_prod(cls):
        return String.equals(cls.PRD, cls.get())
