#!/usr/bin/python
from pandora.commons import String, OS


# def create(name: str, path: str):
def create(name: str = None, path: str = None):
    if String.is_empty(name):
        name = "Artemis"
    if not OS.Path.exists(path):
        path = "/root"

    return f"Hello Creation World! Name: {name}, Path: {path}."
