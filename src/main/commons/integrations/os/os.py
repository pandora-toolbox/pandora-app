import os
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, TextIO, Union, List
import re

from ...stypes import String, Collection


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

    class Shell:
        @staticmethod
        def run(cmd: str = None, args: List[str] = None,
                get_output: bool = False) -> Union[str, None]:
            """
            Run a command in OS. It uses the `subprocess` library.

            :param cmd: command to be runned
            :param args: command arguments as a list of strings
            :param get_output: if the application should return the output
            :return: the possible output as byte of string
            """
            if String.not_empty(cmd):
                import subprocess

                args.insert(0, cmd)  # add cmd as first parameter of the list

                # Here it is decided wether use `subprocess.check_output` or `subprocess.check_call`
                # `subprocess.call` were not used because it would be less convenient since
                # we would need to manually check the return code of each command and handle errors ourselves
                if get_output is True:
                    # `subprocess.check_output` is used because we want to capture the output of the command.
                    # It also has the same error handling as `subprocess.call` (see below)
                    return subprocess.check_output(args)
                else:
                    # `subprocess.check_call` is used to execute a command and raises a CalledProcessError
                    # exception if the command fails.
                    subprocess.check_call(args)

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

        @staticmethod
        def touch(path: str, filename: str) -> str:
            if String.not_empty(filename) and String.not_empty(path):
                full_path: str = f"{path}/{filename}"
                OS.Shell.run("touch", [full_path])

                return full_path
            else:
                raise ValueError("Not possible to create a file since 'path' or 'filename' parameter is empty.")

        @staticmethod
        def mkdir(path: str):
            if String.not_empty(path):
                OS.Shell.run("mkdir", ["-p", path])
            else:
                raise ValueError("Not possible to create a directory since 'path' parameter is empty.")

        # noinspection PyTypeChecker
        @staticmethod
        def subdirs(path: str, recursive: bool = False) -> List[str]:
            if String.not_empty(path):
                directories: List[str] = [dirs for subdir, dirs, files in os.walk(path)]

                if Collection.not_empty(directories):
                    valid_dirs: List[str] = directories[0]
                    for subdir in valid_dirs:
                        if re.search(".*__.*__", str(subdir)) is not None:
                            valid_dirs.remove(subdir)

                        if recursive is True:
                            if path.startswith("/"):
                                full_path = path
                            elif path.endswith("/"):
                                full_path = f"{path}{subdir}"
                            else:
                                full_path = f"{path}/{subdir}"

                            sub_directories = OS.Path.subdirs(full_path, recursive=True)
                            valid_dirs.extend(sub_directories)

                    if path.endswith("/"):
                        return [f"{path}{subdir}" for subdir in directories[0]] or []
                    else:
                        return [f"{path}/{subdir}" for subdir in directories[0]] or []

        @staticmethod
        def files(path: str) -> List[str]:
            if String.not_empty(str(path)):
                __files: List = [files for subdir, dirs, files in os.walk(path)]
                if Collection.not_empty(__files):
                    return ["{}/{}".format(path, subdir) for subdir in __files[0]] or []
                else:
                    return []