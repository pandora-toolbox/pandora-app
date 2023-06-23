from enum import Enum

from pandora.commons.stypes import String
from pandora.toolbox.sdk.pools import ObjectPool


class AppEnvironment(Enum):
    OID: str = "app.preferences.environment"

    DEV = "dev"
    PRD = "prd"

    @classmethod
    def get(cls) -> str:
        return ObjectPool().get(str(cls.OID))

    @classmethod
    def is_dev(cls):
        return String.equals(cls.DEV, cls.get())

    @classmethod
    def is_prod(cls):
        return String.equals(cls.PRD, cls.get())
