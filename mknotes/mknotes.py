#!/usr/bin/python3
import argparse
from os import listdir, makedirs, rmdir, path, remove
from pathlib import Path
from subprocess import call
from typing import Optional

from lib.settings import config


def alter_note(alter_note: dict, config: dict):
    title = alter_note.alter.split(".")[-1]
    
    note_path = path.join(
            config["notes_location"], *alter_note.alter.split(".")[:-1], (title + "." + config["extension"])
    )
    
    if path.exists(path.dirname(note_path)) is False:
        makedirs(path.dirname(note_path))

    if path.isfile(note_path) is False:
        with open(note_path, "w") as note:
            note.write("#{}\n".format(title))

    call([config["editor"], note_path])


def remove_suffix(string: str) -> str:
    return path.splitext(string)[0]


def confirm_choice(msg: Optional[str] = False) -> bool:
    if msg:
        print(msg)

    confirm = None
    while confirm != "c" and confirm != "v":
        confirm = input("[c]Confirm or [v]Void: ")
        if confirm != "c" and confirm != "v":
            print("\n Invalid Option. Please Enter a Valid Option.")

    return True if (confirm == "c") else False


def delete_note(rm_note: dict, config: dict):
    title = rm_note.delete.split(".")[-1]
    
    note_path = path.join(
            config["notes_location"], *rm_note.delete.split(".")[:-1], (title + "." + config["extension"])
    )

    if path.exists(note_path) is False:
        print(f"No note: {rm_note.delete}")
    elif confirm_choice("Do you wish to delete {}".format(rm_note.delete)):
        try:
            remove(note_path)
            if not listdir(path.dirname(note_path)):
                rmdir(path.dirname(note_path))
            print(f"Deleted {rm_note.delete}")
        except:
            print("Could not delete")


def list_notes(config: dict):
    print("TODO")


def parse_args() -> dict:
    arguments = argparse.ArgumentParser(
        description="mknotes. Simple cli tool for creating and managing markdown notes."
    )

    arguments.add_argument(
        "-a", "--alter", dest="alter", type=str, help="Add/Edit note"
    )
    arguments.add_argument(
        "-d", "--delete", dest="delete", type=str, help="Delete note"
    )
    arguments.add_argument(
        "-l", "--list", dest="list", action="store_true", help="list notes"
    )

    args = arguments.parse_args()

    return args


def main():
    arguments = parse_args()

    if arguments.alter:
        alter_note(arguments, config)
    elif arguments.delete:
        delete_note(arguments, config)
    elif arguments.list:
        list_notes(config)


if __name__ == "__main__":
    main()
