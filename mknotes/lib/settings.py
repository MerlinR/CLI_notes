#!/usr/bin/python3
from configparser import ConfigParser
from os import makedirs, path
from shutil import which

DEFAULT_LOC = path.join(path.expanduser("~"), ".mknotes")
CONFIG_FILE_NAME = path.join(DEFAULT_LOC, "mknotes.cfg")
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {
    "notes_location": path.join(DEFAULT_LOC, "notes"),
    "editor": "vim",
    "view-mode": "combo",
    "extension": "md",
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


def _read_config_file(config_file: dict, settings: dict) -> dict:
    config = ConfigParser()
    config.read(config_file)

    if config.has_section(CONFIG_SECTION):
        read_settings = dict(config.items(CONFIG_SECTION))
        settings.update(read_settings)
    return settings


def _write_config_file(config_file: str, config_to_save: dict):
    config = ConfigParser()
    config["settings"] = config_to_save

    with open(config_file, "w") as configfile:
        config.write(configfile)


def _config_error(config: str, message: str):
    raise ValueError("ERROR: {} configuration: {}".format(config, message))


def _validate_editor(tool: str) -> str:
    default_editors = DEFAULT_EDITORS.insert(0, tool)

    for editor in default_editors:
        if which(editor):
            return which(editor)

    _config_error("Editor", "Cannot find usable editor {}".format(default_editors))


def _validate_view(view_mode: str) -> str:
    if view_mode not in VIEW_OPTIONS:
        return options[0]
    else:
        return view_mode


def _validate_extension(extension: str) -> str:
    if extension[:1] == ".":
        extension = extension[1:]
    if extension.lower() in MARKDOWN_EXTENSIONS:
        return extension
    else:
        return valid_extensions[0]


def _getConfig() -> dict:
    settings = DEFAULT_CONFIG
    config_file = path.expanduser(CONFIG_FILE_NAME)

    if path.exists(config_file):
        settings = _read_config_file(config_file, settings)
    else:
        if not path.exists(path.dirname(config_file)):
            makedirs(path.dirname(config_file))

    for note_path in settings["notes_location"].split(","):
        if path.exists(note_path) is False:
            makedirs(note_path)

    if path.exists(settings["editor"]) is False:
        settings["editor"] = _validate_editor(settings["editor"])

    settings["view-mode"] = _validate_view(settings["view-mode"])
    settings["extension"] = _validate_extension(settings["extension"])

    _write_config_file(config_file, settings)
    settings["note_paths"] = settings["notes_location"].split(",")
    return settings


config = _getConfig()
