#!/usr/bin/python3
import os
import pydoc
import sys

import mdv
from lib.definitions import Note
from lib.misc import Color, Style, fontColor, fontReset


class MarkdownParse:
    name = ""
    _notePath = ""

    def __init__(self, note: Note):
        self._note = note
        if not os.path.exists(note.path):
            print(f"{note.name} does not exist")
            sys.exit(1)
        self._configure_mdv()

    def _configure_mdv(self):
        mdv.term_columns = 60

    def _read_raw_markdown(self):
        markdown = None
        with open(self._note.path, "r") as mk:
            markdown = mk.read()
        return markdown

    def print(self):
        rows, columns = os.popen("stty size", "r").read().split()
        print(f"{fontColor(style = Style.ITALIC)}{self._note.min_path}{fontReset()}")
        raw_markdown = self._read_raw_markdown()
        if len(raw_markdown) > int(rows):
            pydoc.pipepager(mdv.main(raw_markdown), cmd="less -R")
        else:
            print(mdv.main(raw_markdown))
