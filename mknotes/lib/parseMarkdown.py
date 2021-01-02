#!/usr/bin/python3
import os
import sys

class MarkdownParse():
    name = ""
    _notePath = ""

    def __init__(self, notePath: str):
        self._notePath = notePath
        if not os.path.exists(notePath):
            print(f"{notePath} does not exist")
            sys.exit(1)
        self.name = os.path.basename(notePath)

    def print(self):
        print(name)
