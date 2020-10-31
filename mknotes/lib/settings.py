#!/usr/bin/python
from configparser import ConfigParser
from os import path
from shutil import which

DEFAULT_LOC = "~/.mknotes"
CONFIG_FILE_NAME = path.join(DEFAULT_LOC, "mknotes.cfg")
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {
    "notes_location": path.join(DEFAULT_LOC, "notes"),
    "editor": "vim",
    "view-mode": "combo",
}


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
    default_editors = [tool, "vim", "nano"]

    for editor in default_editors:
        if which(editor):
            return which(editor)

    _config_error("Editor", "Cannot find usable editor {}".format(default_editors))


def _validate_view(view_mode: str) -> str:
    options = ["interactive", "dump", "combo"]
    if view_mode not in options:
        return "combo"
    else:
        return view_mode


def _getConfig() -> dict:
    settings = DEFAULT_CONFIG
    config_file = path.expanduser(CONFIG_FILE_NAME)

    if path.exists(config_file):
        settings = _read_config_file(config_file, settings)
    else:
        if not path.exists(path.dirname(config_file)):
            os.makedirs(path.dirname(config_file))

    if path.exists(settings["editor"]) is False:
        settings["editor"] = _validate_editor(settings["editor"])

    settings["view-mode"] = _validate_view(settings["view-mode"])

    _write_config_file(config_file, settings)
    return settings


config = _getConfig()
