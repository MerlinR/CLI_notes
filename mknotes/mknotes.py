#!/usr/bin/python3
import argparse
import os
import re
import sys
from pathlib import Path
from subprocess import call
from typing import Optional

from lib.definitions import Note
from lib.misc import Color, Style, fontColor, fontReset
from lib.parseMarkdown import MarkdownParse
from lib.settings import config


def remove_suffix(string: str) -> str:
    return os.path.splitext(string)[0]


def note_selection(msg: str, options: list) -> int:
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
        if option not in options:
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


def get_note_contents(path: str) -> str:
    regObj = re.compile(f"^\s*#+.*")
    contents = ""

    with open(path) as f:
        for line in f:
            if regObj.match(line):
                level = line.count("#")
                contents += "  " * level
                contents += line.replace("#", "").strip() + "\n"

    return contents


def get_note_list() -> list:
    def search_all_notes(cur_path: str, indent: int = 0, dir_list=[]):
        prev_item = ""

        for indx, item in enumerate(sorted(os.listdir(cur_path))):
            if "{}.{}".format(prev_item, config.get("extension")) == item:
                continue
            if os.path.isdir(os.path.join(cur_path, item)) and "{}.{}".format(
                item, config.get("extension")
            ) in os.listdir(cur_path):
                # Note with subfolder
                dir_list.append(
                    Note(
                        os.path.join(cur_path, f"{item}.{config.get('extension')}"),
                        indent,
                    )
                )
            elif item.endswith(config.get("markdown_extensions")):
                # Note Only
                dir_list.append(Note(os.path.join(cur_path, item), indent))

            if os.path.isdir(os.path.join(cur_path, item)):
                search_all_notes(
                    os.path.join(cur_path, item), indent=indent + 1, dir_list=dir_list
                )
            prev_item = item
        return dir_list

    notes = []
    for note_path in config.get("note_paths"):
        notes.extend(search_all_notes(note_path, dir_list=[]))
    # result = list(Path(config["note_paths"][0]).rglob(f"*.{config['extension']}"))
    # for found in sorted(result):
    #    notes.append(Note(str(found)))

    count = 1
    for note in notes:
        note.count_id = count
        note.contents = get_note_contents(note.path)
        count += 1
    return notes


def view_note(view_note: dict):
    if os.path.isfile(view_note.view):
        relevent_notes = [Note(view_note.view)]
    else:
        relevent_notes = search_note_by_name(view_note.view)
    found_note = None
    if not relevent_notes:
        print(f"No matching note called or containing: {view_note.view}")
        deep_search_within_note(view_note.view)
    elif len(relevent_notes) == 1:
        found_note = relevent_notes[0]
    else:
        list_notes(relevent_notes)
        options = [note.count_id for note in relevent_notes]
        choice = note_selection(f"Please select a note: {options}", options)

        found_note = [note for note in relevent_notes if note.count_id == choice][0]

    if found_note:
        MarkdownParse(found_note).print()


def search_note_by_name(name) -> list:
    notes = get_note_list()
    relevent_notes = []
    regObj = re.compile(f".*{name}.*")
    for note in notes:
        if regObj.match(str(note.min_path)):
            relevent_notes.append(note)
        elif name.isdigit() and int(name) == note.count_id:
            relevent_notes.append(note)

    return relevent_notes


def list_notes(note_list: list, list_contents: bool = False):
    note_indx = 0
    note_indent = 0
    ident_str = f"{fontColor(Color.GREY)} - {fontReset()}"

    for note in note_list:
        note_name = os.path.basename(note.path)
        note_indent = note.indent

        print(
            " "
            + f"{ident_str}{fontColor()}{remove_suffix(note.min_path)}{fontReset()}",
            end="",
        )

        print(
            f"{fontColor(Color.GREY, style = Style.ITALIC)}({note.count_id}){fontReset()}"
        )

        if list_contents:
            for line in note.contents.splitlines():
                print(
                    "  " * (note_indent + 1)
                    + f"{fontColor(setcolor = Color.YELLOW)}{line}{fontReset()}"
                )
        if note.extra_info:
            for line in note.extra_info.splitlines():
                print(
                    "  " * (note_indent + 1)
                    + f"{fontColor(setcolor = Color.RED)}{line}{fontReset()}"
                )

#TODO Fix
def alter_note(alter_note: dict):
    title = alter_note.alter.split(".")[-1]

    note_path = os.path.join(
        config.get("note_paths")[0],
        *alter_note.alter.split(".")[:-1],
        (title + "." + config.get("extension")),
    )

    if os.path.exists(os.path.dirname(note_path)) is False:
        makedirs(os.path.dirname(note_path))

    if os.path.isfile(note_path) is False:
        with open(note_path, "w") as note:
            note.write("#{}\n".format(title))

    call([config.get("editor"), note_path])


def configure_config(arguments: dict):
    call([config.get("editor"), config.config_path])


def delete_note(rm_note: dict):
    relevent_notes = search_note_by_name(rm_note.delete)
    choice = False

    if len(relevent_notes) > 1:
        list_notes(relevent_notes)
        options = [note.count_id for note in relevent_notes]
        choice = note_selection(f"Please select a note: {options}", options)
    elif confirm_choice("Do you wish to delete {}".format(relevent_notes[0].min_path)):
        choice = relevent_notes[0].count_id
    elif not choice:
        print(f"Not deleting: {rm_note.delete}")
        return

    note = [note for note in relevent_notes if note.count_id == choice][0]
    try:
        os.remove(note_path)
        print(f"Deleted {note.min_path}")
    except:
        print("Could not delete")


def search_note(search_note: dict):
    relevent_notes = search_note_by_name(search_note.search)
    list_notes(relevent_notes, list_contents=True)


def deep_search_within_note(search_text: str):
    notes = get_note_list()
    regObj = re.compile(f".*{search_text}.*")
    relevent_notes = []

    for note in notes:
        found_match = False
        with open(note.path) as f:
            for indx, line in enumerate(f):
                if regObj.match(line):
                    note.extra_info = note.extra_info + f"{indx+1}: {line}"
                    found_match = True
        if found_match:
            relevent_notes.append(note)

    list_notes(relevent_notes)


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
        "-l", "--list", dest="list", action="store_true", help="list notes"
    )
    arguments.add_argument(
        "-ll",
        "--sub-list",
        dest="sublist",
        action="store_true",
        help="list notes and titles",
    )
    arguments.add_argument(
        "-d", "--delete", dest="delete", type=str, help="Delete note"
    )
    arguments.add_argument(
        "-s", "--search", dest="search", type=str, help="Search for note by title"
    )
    arguments.add_argument(
        "-ds",
        "--deep-search",
        dest="dsearch",
        type=str,
        help="Search for note by content",
    )
    arguments.add_argument(
        "-c",
        "--configure",
        dest="configure",
        action="store_true",
        help="Change the configurations",
    )

    args = arguments.parse_args()

    if len(sys.argv) < 2:
        args.list = True

    return args


def main():
    arguments = parse_args()

    if arguments.view:
        view_note(arguments)
    elif arguments.alter:
        alter_note(arguments)
    elif arguments.delete:
        delete_note(arguments)
    elif arguments.list:
        list_notes(get_note_list())
    elif arguments.sublist:
        list_notes(get_note_list(), list_contents=True)
    elif arguments.search:
        search_note(arguments)
    elif arguments.dsearch:
        deep_search_within_note(arguments.dsearch)
    elif arguments.configure:
        configure_config(arguments)


if __name__ == "__main__":
    main()
