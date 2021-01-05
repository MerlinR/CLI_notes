#!/usr/bin/python3
import argparse
import os
import sys
from pathlib import Path
from subprocess import call
from typing import Optional

from lib.misc import colorText, Color, Style
from lib.definitions import Note
from lib.settings import config, CONFIG_FILE_NAME
from lib.parseMarkdown import MarkdownParse


def remove_suffix(string: str) -> str:
    return os.path.splitext(string)[0]


def note_selection(msg: str, options: list) -> bool:
    if msg:
        print(msg)

    option = None
    while option not in options:
        option = input("Note selection or [q]uit: ")
        try:
            option = int(option)
        except:
            pass
        if option == "q":
            sys.exit(1)
        print(f"\n Invalid Option. {msg}")

    return option


def confirm_choice(msg: Optional[str] = False) -> bool:
    if msg:
        print(msg)

    confirm = None
    while confirm != "c" and confirm != "v":
        confirm = input("[c]Confirm or [v]Void: ")
        if confirm != "c" and confirm != "v":
            print("\n Invalid Option. Please Enter a Valid Option.")

    return True if (confirm == "c") else False


def get_note_list(config: dict):
    def search_all_notes(cur_path: str, indent: int = 0, dir_list=[]):
        prev_item = ""

        for indx, item in enumerate(sorted(os.listdir(cur_path))):

            if "{}.{}".format(prev_item, config["extension"]) == item:
                continue

            if os.path.isdir(os.path.join(cur_path, item)) and "{}.{}".format(
                item, config["extension"]
            ) in os.listdir(cur_path):
                # Note with subfolder
                dir_list.append(Note(os.path.join(cur_path, item), indent))
            elif os.path.isdir(os.path.join(cur_path, item)):
                # Subfolder only
                dir_list.append(Note(os.path.join(cur_path, item), indent, folder=True))
            else:
                # Note Only
                dir_list.append(Note(os.path.join(cur_path, item), indent))

            if os.path.isdir(os.path.join(cur_path, item)):
                search_all_notes(
                    os.path.join(cur_path, item), indent=indent + 1, dir_list=dir_list
                )
            prev_item = item
        return dir_list

    notes = search_all_notes(config["notes_location"])
    count = 1
    for note in notes:
        if not note.folder:
            note.count_id = count
            count += 1

    return notes


def view_note(view_note: dict, config: dict):
    relevent_notes = search_note_by_name(view_note.view, config)
    found_note = None
    if not relevent_notes:
        print(f"No matching notes for {search_note.search}")
    elif len(relevent_notes) == 1:
        found_note = relevent_notes[0]
    else:
        list_notes(relevent_notes, config, full_path=True)
        options = []
        for note in relevent_notes:
            options.append(note.count_id)
            options.append(note.name)
        choice = note_selection(f"Please select a note: {options}", options)

        for note in relevent_notes:
            if isinstance(choice, int):
                if note.count_id == choice:
                    found_note = note
                    break
            else:
                if note.name == choice:
                    found_note = note
                    break

    MarkdownParse(found_note).print()


def search_note_by_name(name, config: dict):
    notes = get_note_list(config)
    relevent_notes = []
    for note in notes:
        if name in str(note.min_path):
            relevent_notes.append(note)
    return relevent_notes


def list_notes(
    note_list: list, config: dict, full_path: bool = False, list_contents: bool = False
):
    note_indx = 0
    note_indent = 0
    ident_str = f"{colorText.color(Color.GREY)}--{colorText.reset()}"

    for note in note_list:
        note_name = os.path.basename(note.path)
        note_indent = note.indent

        if full_path:
            print(
                " "
                + f"{colorText.color()}{remove_suffix(note.min_path)}{colorText.reset()}",
                end="",
            )
        else:
            print(
                " "
                + f"{ident_str}" * note_indent
                + f"{colorText.color()}{remove_suffix(note_name)}{colorText.reset()}",
                end="",
            )

        if not note.folder:
            print(
                f"{colorText.color(Color.GREY, style = Style.ITALIC)}({note.count_id}){colorText.reset()}"
            )
        else:
            print(f"*{colorText.reset()}")


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

def configre_notes(arguments: dict, config: dict):
    call([config["editor"], CONFIG_FILE_NAME])


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


def search_note(search_note: dict, config: dict):
    relevent_notes = search_note_by_name(search_note.search, config)
    list_notes(relevent_notes, config, full_path=True)


def parse_args() -> dict:
    arguments = argparse.ArgumentParser(
        description="mknotes. Simple cli tool for creating and managing markdown notes."
    )

    arguments.add_argument(
        dest="view", nargs="?", type=str, help="View specific note, will do a search"
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
    arguments.add_argument(
        "-s", "--search", dest="search", type=str, help="Search for note by title"
    )
    arguments.add_argument(
        "-c", "--configure", dest="configure", action="store_true", help="Change the configurations"
    )

    args = arguments.parse_args()

    if len(sys.argv) < 2:
        args.list = True

    return args


def main():
    arguments = parse_args()

    if arguments.view:
        view_note(arguments, config)
    elif arguments.search:
        search_note(arguments, config)
    elif arguments.alter:
        alter_note(arguments, config)
    elif arguments.delete:
        delete_note(arguments, config)
    elif arguments.list:
        list_notes(get_note_list(config), config)
    elif arguments.configure:
        configre_notes(arguments, config)


if __name__ == "__main__":
    main()
