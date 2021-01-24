#!/usr/bin/python3

import hashlib
import os
import re
from dataclasses import dataclass
from typing import List

from notes.lib.settings import config


@dataclass
class Contents:
    title: str
    indent: int


class Note:
    path: str = ""
    indent: int = 0
    name: str = ""
    min_path: str = ""
    content_list: List[Contents] = None
    extra_info: list = []
    count_id: int = -1
    id: str = None

    def __init__(self, path, indent=0):
        self.path = path
        self.id = hashlib.sha1(self.path.encode("utf-8")).hexdigest()[:6]
        for path in config.get("note_paths"):
            if path in self.path:
                self.min_path = (os.path.relpath(self.path, path)).replace("/", ".")
        self.name = os.path.splitext(os.path.basename(self.path))[0]
        self.indent = indent

    @property
    def contents(self) -> List[Contents]:
        regObj = re.compile(f"^\s*#+.*")

        if not self.content_list:
            self.content_list = []
            with open(self.path) as note_file:
                for line in note_file:
                    if regObj.match(line):
                        level = line.count("#")
                        self.content_list.append(
                            Contents(line.replace("#", "").strip(), level)
                        )

        return self.content_list

    def text_search(self, substring: str) -> extra_info:
        if self.extra_info:
            return self.extra_info
        matches = []
        regex_str = (
            "((?:.*\n){0,"
            + config.get("search_n_lines_up")
            + "}.*"
            + substring
            + ".*"
            + "(?:.*\n){0,"
            + config.get("search_n_lines_down")
            + "})"
        )
        with open(self.path) as note_file:
            matches = re.findall(regex_str, note_file.read(), flags=re.IGNORECASE)

        # Remove the markdown code tags (```)
        self.extra_info = [match.replace("```\n", "") for match in matches]
        return self.extra_info
