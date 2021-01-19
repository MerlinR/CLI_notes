#!/usr/bin/python3
from configparser import ConfigParser
from os import makedirs, path
from shutil import which
from typing import Optional

DEFAULT_LOC = path.join(path.expanduser("~"), ".notes")
CONFIG_FILE_NAME = path.join(DEFAULT_LOC, "notes.cfg")
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {
    "notes_location": path.join(DEFAULT_LOC, "notes"),
    "editor": "vim",
    "view-mode": "combo",
    "extension": "md",
    "color_scheme": "637.2829",
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
                if self._confirm_choice(f"Path {note_path} does not exist, create it?"):
                    makedirs(note_path)
                    self._extra["note_paths"].append(note_path)
            else:
                self._extra["note_paths"].append(note_path)
        self._config["notes_location"] = ",".join(self._extra["note_paths"])

        if path.exists(self._config["editor"]) is False:
            self._config["editor"] = self._validate_editor(self._config["editor"])

        self._config["view-mode"] = self._validate_view(self._config["view-mode"])
        self._config["extension"] = self._validate_extension(self._config["extension"])

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

    def _config_error(self, message: str):
        raise ValueError("ERROR: {} configuration: {}".format(self._config, message))

    def _validate_editor(self, tool: str) -> str:
        default_editors = DEFAULT_EDITORS
        if which(tool.split(" ")[0]):
            return tool
        for editor in default_editors:
            if which(editor):
                print(f"ERROR: {tool} invalid, using {editor}")
                return which(editor)

        _config_error("Editor", "Cannot find usable editor {}".format(default_editors))

    def _validate_view(self, view_mode: str) -> str:
        if view_mode not in VIEW_OPTIONS:
            return options[0]
        else:
            return view_mode

    def _validate_extension(self, extension: str) -> str:
        if extension[:1] == ".":
            extension = extension[1:]
        if extension.lower() in MARKDOWN_EXTENSIONS:
            return extension
        else:
            return valid_extensions[0]

    def get(self, key: str) -> str:
        if self._config.get(key):
            return self._config[key]
        else:
            return self._extra.get(key)
    
    def set(self, key: str, value: str):
        if self._config.get(key):
            self._config[key] = value
        elif self._extra.get(key):
            self._extra[key] = value

    def _confirm_choice(self, msg: Optional[str] = False) -> bool:
        if msg:
            print(msg)

        confirm = None
        while confirm != "c" and confirm != "v":
            confirm = input("[c]Confirm or [v]Void: ")
            if confirm != "c" and confirm != "v":
                print("\n Invalid Option. Please Enter a Valid Option.")

        return True if (confirm == "c") else False


config = Settings()
