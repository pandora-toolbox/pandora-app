from .manifest import *
from functools import cache

from ...commons.integrations import OS


class Constants:
    """
    Constant Class that address the issue where we want to cache some objects nested in a class.
    The cache decorator caches the method object instead of the method's return value.
    By using a class method decorated with cache to cache the return value of the `<property>()` method,
      and defining a property that returns the cached value, we can ensure that the correct value
      is returned when calling Constants.<property>.
    """
    # TODO: Load this locally on venv
    OS.Environment.load_vars(f"{OS.Path.cwd()}/.env")

    # Define a nested class to hold the cached values
    class __Values:
        # Define a class method to retrieve the cached value of the home() method
        @classmethod
        @cache
        def home(cls) -> str:
            return OS.Environment.var("PANDORA_HOME")

    # Define a property that returns the cached value of the home() method
    home: str = __Values.home()

