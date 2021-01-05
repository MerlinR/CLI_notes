#!/usr/bin/python3
import os
import sys

from lib.misc import Note 

class MarkdownParse():
    name = ""
    _notePath = ""

    def __init__(self, note: Note):
        self._note = note
        if not os.path.exists(note.path):
            print(f"{note.name} does not exist")
            sys.exit(1)
    
    def print(self):
        print(self._note)
