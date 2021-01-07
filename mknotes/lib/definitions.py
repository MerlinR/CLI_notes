#!/usr/bin/python3

import hashlib
import os
from dataclasses import dataclass

from lib.settings import config


@dataclass
class Note:
    path: str
    indent: int = 0
    name: str = ""
    min_path: str = ""
    contents: str = ""
    extra_info: str = ""
    count_id: int = -1
    id: str = None

    def __post_init__(self):
        self.id = hashlib.sha1(self.path.encode("utf-8")).hexdigest()[:6]
        for path in config.get("note_paths"):
            if path in self.path:
                self.min_path = (os.path.relpath(self.path, path)).replace("/", ".")
        self.name = os.path.splitext(os.path.basename(self.path))[0]
