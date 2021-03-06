#!/usr/bin/python3
import os
import pydoc
import sys

import mdv

from notes.lib.definitions import Note
from notes.lib.misc import Color, Style, fontColor, fontReset
from notes.lib.settings import config


class MarkdownParse:
    name = ""
    _notePath = ""
    # MDV settings
    _MDV_theme_id = config.get("color_scheme")
    _MDV_headers = "1-"

    def __init__(self, note: Note):
        self._note = note
        if not os.path.exists(note.path):
            print(f"{note.name} does not exist")
            sys.exit(1)

    def _read_raw_markdown(self):
        markdown = None
        with open(self._note.path, "r") as mk:
            markdown = mk.read()
        return markdown

    def print(self):
        rows, columns = os.popen("stty size", "r").read().split()
        print(f"{fontColor(style = Style.ITALIC)}{self._note.min_path}{fontReset()}")

        raw_markdown = self._read_raw_markdown()

        mdv.term_columns = 60
        if config.get("view-mode") == "interactive":
            pydoc.pipepager(
                mdv.main(
                    raw_markdown,
                    theme=self._MDV_theme_id,
                    header_nrs=self._MDV_headers,
                ),
                cmd="less -R",
            )
        elif config.get("view-mode") == "combo" and len(raw_markdown) > int(rows):
            pydoc.pipepager(
                mdv.main(
                    raw_markdown,
                    theme=self._MDV_theme_id,
                    header_nrs=self._MDV_headers,
                ),
                cmd="less -R",
            )
        else:
            print(mdv.main(raw_markdown))
