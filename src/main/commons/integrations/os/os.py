import os
from typing import Optional


# noinspection PyTypeChecker
class OS:
    @staticmethod
    def var(name: str = None) -> Optional[str]:
        """Get an Environment Variable. If it was not found, 'None' is returned"""
        return os.environ.get(name)
