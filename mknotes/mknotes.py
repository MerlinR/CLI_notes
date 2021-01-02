#!/usr/bin/python3
import argparse
import os
import sys
from pathlib import Path
from subprocess import call
from typing import Optional

from lib.misc import colorText, Color, Style
from lib.settings import config


def alter_note(alter_note: dict, config: dict):
    title = alter_note.alter.split(".")[-1]

    note_path = os.path.join(
        config["notes_location"],
        *alter_note.alter.split(".")[:-1],
        (title + "." + config["extension"]),
    )

    if os.path.exists(os.path.dirname(note_path)) is False:
        makedirs(os.path.dirname(note_path))

    if os.path.isfile(note_path) is False:
        with open(note_path, "w") as note:
            note.write("#{}\n".format(title))

    call([config["editor"], note_path])


def remove_suffix(string: str) -> str:
    return os.path.splitext(string)[0]


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

    note_path = os.path.join(
        config["notes_location"],
        *rm_note.delete.split(".")[:-1],
        (title + "." + config["extension"]),
    )

    if os.path.exists(note_path) is False:
        print(f"No note: {rm_note.delete}")
    elif confirm_choice("Do you wish to delete {}".format(rm_note.delete)):
        try:
            os.remove(note_path)
            if not os.os.listdir(os.path.dirname(note_path)):
                os.rmdir(os.path.dirname(note_path))
            print(f"Deleted {rm_note.delete}")
        except:
            print("Could not delete")


def list_notes(config: dict):
    def print_notes(cur_path: str, indent: int = 0):
        prev_item = ""
        ident_str = f"{colorText.color(Color.GREY)}--{colorText.reset()}"

        for indx, item in enumerate(sorted(os.listdir(cur_path))):

            if "{}.{}".format(prev_item, config["extension"]) == item:
                continue

            if os.path.isdir(os.path.join(cur_path, item)) and "{}.{}".format(
                item, config["extension"]
            ) in os.listdir(cur_path):
                # Note with subfolder
                print(
                    f"{ident_str}" * indent
                    + f"{colorText.color()}{remove_suffix(item)}{colorText.reset()}"
                )
            elif os.path.isdir(os.path.join(cur_path, item)):
                # Subfolder only
                print(f"{ident_str}" * indent + f"{colorText.color(style = Style.ITALIC)}*{remove_suffix(item)}{colorText.reset()}")
            else:
                # Note Only
                print(f"{ident_str}" * indent + f"{colorText.color()}{remove_suffix(item)}{colorText.reset()}")

            if os.path.isdir(os.path.join(cur_path, item)):
                print_notes(os.path.join(cur_path, item), indent + 1)
            prev_item = item

    print_notes(config["notes_location"])


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

    if len(sys.argv) < 2:
        arguments.print_usage()
        sys.exit(1)

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
