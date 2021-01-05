#!/usr/bin/python3

import hashlib
import os
from dataclasses import dataclass

from lib.settings import config


@dataclass
class Note:
    path: str
    indent: int
    directory: bool = False
    name: str = ""
    min_path: str = ""
    extra_info = ""
    count_id: int = -1
    id: str = None

    def __post_init__(self):
        self.id = hashlib.sha1(self.path.encode("utf-8")).hexdigest()[:6]
        self.min_path = (os.path.relpath(self.path, config["notes_location"])).replace(
            "/", "."
        )
        self.name = os.path.splitext(os.path.basename(self.path))[0]
