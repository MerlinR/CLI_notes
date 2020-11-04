#!/usr/bin/python3
import argparse
from os import listdir, path, remove
from pathlib import Path
from subprocess import call
from typing import Dict, Optional

from lib.settings import config


def alter_note(alter_note: Dict, config: Dict):
    alter_note.alter = path.splitext(alter_note.alter)[0]
    note_path = path.join(
        config["notes_location"], "{}.{}".format(alter_note.alter, "md")
    )

    if path.isfile(note_path) is False:
        with open(note_path, "w") as note:
            note.write("#{}".format(alter_note.alter))

    call([config["editor"], note_path])


def confirm_choice(msg: Optional[str] = False) -> bool:
    if msg:
        print(msg)

    confirm = None
    while confirm != "c" and confirm != "v":
        confirm = input("[c]Confirm or [v]Void: ")
        if confirm != "c" and confirm != "v":
            print("\n Invalid Option. Please Enter a Valid Option.")

    return True if (confirm == "c") else False


def delete_note(rm_note: Dict, config: Dict):
    rm_note.delete = path.splitext(rm_note.delete)[0]
    note_path = path.join(
        config["notes_location"], "{}.{}".format(rm_note.delete, "md")
    )

    if path.exists(note_path) is False:
        print(f"No note called {rm_note.delete}")
    elif confirm_choice("Do you wish to delete {}".format(rm_note.delete)):
        remove(note_path)


def parse_args() -> Dict:
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
