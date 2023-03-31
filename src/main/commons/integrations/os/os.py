import os
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, TextIO, Union

from src.main.commons.stypes import String


# noinspection PyTypeChecker
class OS:
    class Environment:
        @staticmethod
        def var(name: str = None) -> Optional[str]:
            """Get an Environment Variable. If it was not found, 'None' is returned"""
            return os.environ.get(name)

        @staticmethod
        def load_vars(dotenv_path: str = None):
            """Load a `.env` file"""
            from dotenv import load_dotenv

            if OS.Path.exists(dotenv_path):
                load_dotenv(dotenv_path=Path(dotenv_path))
            else:
                # TODO: Implement logging here
                pass

        @staticmethod
        def expand_vars(text: Union[TextIO, TextIOWrapper] = None) -> str:
            """
            Expand Environment Variables in a file stream and return the file content with all variables replaced.
            """
            if text is not None:
                return os.path.expandvars(text.read())
            else:
                raise ValueError("Error while trying to expand Environment Variables: Text is 'None'.")

    class Path:
        @staticmethod
        def exists(path: str = None) -> bool:
            """Check if a Path exists"""
            return String.not_empty(path) and os.path.exists(path)

        @staticmethod
        def cwd():
            """Return the Absolute Path of the Current Working Directory."""
            import pathlib
            return str(pathlib.Path().resolve())
