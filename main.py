#!/bin/python
import sys

from src.main.sdk import PandoraApp


if __name__ == "__main__":
    app = PandoraApp()
    print(app.run(sys.argv[1:]))
