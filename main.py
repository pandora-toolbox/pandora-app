#!/bin/python
import sys

from pandora.toolbox import ToolboxApp


def run(args: list[str]):
    """
    The app can be called from anywhere like this...
    """
    app = ToolboxApp()
    return app.run(args)


if __name__ == "__main__":
    """
    ... or can be called from a main, like this :D
    """
    print(run(sys.argv[1:]))
