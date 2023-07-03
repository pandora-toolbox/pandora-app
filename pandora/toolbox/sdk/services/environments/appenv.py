from enum import Enum
from typing import Optional

from pandora.commons.stypes import String
from pandora.commons.stypes.enums import SerializableEnum
from pandora.toolbox.sdk.constants import Constants
from pandora.toolbox.sdk.pools import ObjectPool


class AppEnvironment(SerializableEnum):
    OID: str = "app.preferences.environment"

    DEV = "dev"
    PRD = "prd"

    @classmethod
    def get(cls):
        env: Enum = ObjectPool().get(cls.OID.value)

        if env is None:  # Object do not exist on ObjectPool
            env = cls.get_from(Constants.RUNTIME_ENV)

            if env is None:  # Object do not exist as Environment Variable
                raise RuntimeError(f"Unknown environment '{env}'.")
            else:  # Object exists as Environment Variable and will be placed at the ObjectPool
                ObjectPool().add(key=cls.OID.value, obj=env)

        return env

    @classmethod
    def is_dev(cls):
        return String.equals(cls.DEV, cls.get())

    @classmethod
    def is_prod(cls):
        return String.equals(cls.PRD, cls.get())
