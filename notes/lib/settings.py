#!/usr/bin/python3
from configparser import ConfigParser
from os import makedirs, path
from shutil import which
from typing import List, Optional

DEFAULT_LOC = path.join(path.expanduser("~"), ".notes")
CONFIG_FILE_NAME = path.join(DEFAULT_LOC, "notes.cfg")
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {
    "notes_location": path.join(DEFAULT_LOC, "notes"),
    "editor": "vim",
    "view-mode": "combo",
    "extension": "md",
    "color_scheme": "637.2829",
    "search_n_lines_up": 1,
    "search_n_lines_down": 1,
}

MARKDOWN_EXTENSIONS = (
    "md",
    "markdown",
    "mdown",
    "mkdn",
    "mkd",
    "mdwn",
    "mdtxt",
    "mdtext",
)
VIEW_OPTIONS = (
    "combo",
    "dump",
    "interactive",
)
DEFAULT_EDITORS = (
    "vim",
    "nano",
)


class Settings:
    config_path = str(path.expanduser(CONFIG_FILE_NAME))
    _config = DEFAULT_CONFIG
    _extra = {}

    def __init__(self):
        if path.exists(self.config_path):
            self._read_config_file()
        else:
            if not path.exists(path.dirname(self.config_path)):
                makedirs(path.dirname(self.config_path))

        self._extra["note_paths"] = []
        for note_path in self._config["notes_location"].split(","):
            if path.exists(note_path) is False:
                if note_path == path.join(DEFAULT_LOC, "notes":
                    makedirs(note_path)
                    self._extra["note_paths"].append(note_path)
                elif self._confirm_choice(f"Path {note_path} does not exist, create it?"):
                    makedirs(note_path)
                    self._extra["note_paths"].append(note_path)
            else:
                self._extra["note_paths"].append(note_path)
        self._config["notes_location"] = ",".join(self._extra["note_paths"])

        self._validate_configurations(self._config)

        self._extra["markdown_extensions"] = MARKDOWN_EXTENSIONS
        self._extra["primary_note_dir"] = self._extra["note_paths"][0]
        self._write_config_file()

    def _read_config_file(self):
        config = ConfigParser()
        config.read(self.config_path)

        if config.has_section(CONFIG_SECTION):
            read_settings = dict(config.items(CONFIG_SECTION))
            self._config.update(read_settings)

    def _write_config_file(self):
        config = ConfigParser()
        config["settings"] = self._config

        with open(self.config_path, "w") as config_file:
            config.write(config_file)

    def _config_error(self, config: str, message: str):
        raise ValueError("ERROR: {} configuration: {}".format(config, message))

    def _validate_configurations(self, new_config: dict = None, all: bool = False):
        for configuration, value in new_config.items():
            if configuration == "editor" or all:
                self._validate_editor(value)
            elif configuration == "view-mode" or all:
                self._validate_view(value)
            elif configuration == "lines" or all:
                self._validate_lines(value)
            elif configuration == "search_n_lines_up" or all:
                self._validate_lines([value, self._config["search_n_lines_down"]])
            elif configuration == "search_n_lines_down" or all:
                self._validate_lines([self._config["search_n_lines_up"], value])
            elif configuration == "extension" or all:
                self._validate_extension(value)

    def _validate_editor(self, tool: str):
        default_editors = DEFAULT_EDITORS
        if which(tool.split(" ")[0]):
            self._set("editor", tool)
            return
        for editor in default_editors:
            if which(editor):
                print(f"ERROR: {tool} invalid, using {editor}")
                self._set("editor", which(editor))
                return

        self._config_error(
            "Editor", "Cannot find usable editor {}".format(default_editors)
        )

    def _validate_view(self, view_mode: str):
        if view_mode not in VIEW_OPTIONS:
            self._set("view-mode", VIEW_OPTIONS[0])
        else:
            self._set("view-mode", view_mode)

    def _validate_lines(self, lines: List[int]):
        newLines = []
        for line in range(len(lines)):
            if line > 0 and line < 5:
                newLines.append(line)
            else:
                newLines.append(1)
        if len(newLines) < 2:
            newLines.append(1)

        self._set("search_n_lines_up", newLines[0])
        self._set("search_n_lines_down", newLines[1])

    def _validate_extension(self, extension: str):
        if extension[:1] == ".":
            extension = extension[1:]
        if extension.lower() in MARKDOWN_EXTENSIONS:
            self._set("extension", extension)
        else:
            self._set("extension", MARKDOWN_EXTENSIONS[0])

    def _confirm_choice(self, msg: Optional[str] = False) -> bool:
        if msg:
            print(msg)

        confirm = None
        while confirm != "c" and confirm != "v":
            confirm = input("[c]Confirm or [v]Void: ")
            if confirm != "c" and confirm != "v":
                print("\n Invalid Option. Please Enter a Valid Option.")

        return True if (confirm == "c") else False

    def get_config_options(self) -> List[str]:
        return DEFAULT_CONFIG.keys()

    def get(self, key: str) -> str:
        if self._config.get(key):
            return self._config[key]
        else:
            return self._extra.get(key)

    def _set(self, key: str, value: str):
        if self._config.get(key):
            self._config[key] = value
        elif self._extra.get(key):
            self._extra[key] = value

    def set(self, key: str, value: str, save: bool = True):
        if self._config.get(key):
            self._validate_configurations({key: value})
            if save:
                self._write_config_file()
        elif self._extra.get(key):
            self._extra[key] = value


config = Settings()
