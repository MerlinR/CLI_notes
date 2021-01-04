#!/usr/bin/python3

from enum import Enum
from dataclasses import dataclass
import os
import hashlib

from lib.settings import config

@dataclass
class Note:
    path: str
    indent: int
    folder: bool = False
    name: str = ""
    min_path: str = ""
    count_id: int = -1
    id: str = None

    def __post_init__(self):
        self.id = hashlib.sha1(self.path.encode("utf-8")).hexdigest()[:6]
        self.min_path = (os.path.relpath(self.path, config["notes_location"])).replace("/",".")
        self.name = os.path.splitext(os.path.basename(self.path))[0]



class Color(Enum):
    GREY = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


class Style(Enum):
    ENDC = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    RAPIDBLINK = 6


class colorText:
    def color(
        setcolor: Color = Color.WHITE, bright: bool = False, style: Style = Style.ENDC
    ):
        colorCode = setcolor.value

        if bright:
            colorCode = colorCode + 90
        else:
            colorCode = colorCode + 30
        return f"\033[{style.value};{colorCode}m"

    def reset():
        return f"\033[0m"
