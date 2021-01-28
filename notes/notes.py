#!/usr/bin/python3
import argparse
import os
import re
import sys
from pathlib import Path
from subprocess import call
from types import SimpleNamespace
from typing import List, Optional

from notes.lib.definitions import Note
from notes.lib.misc import Color, Style, fontColor, fontReset
from notes.lib.parseMarkdown import MarkdownParse
from notes.lib.settings import config

_version = 1.0


def remove_suffix(string: str) -> str:
    return os.path.splitext(string)[0]


def note_selection(note_list: List[Note]) -> Note:
    if len(note_list) == 1:
        return note_list[0]
    elif len(note_list) == 0:
        return None

    list_notes(note_list)
    options = [note.count_id for note in note_list]
    msg = f"Pleae Select Note: {options}"
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

    return (
        [note for note in note_list if note.count_id == option][0] if option else None
    )


def confirm_choice(msg: Optional[str] = False) -> bool:
    if msg:
        print(msg)

    confirm = None
    while confirm != "c" and confirm != "v":
        confirm = input("[c]Confirm or [v]Void: ")
        if confirm != "c" and confirm != "v":
            print("\n Invalid Option. Please Enter a Valid Option.")

    return True if (confirm == "c") else False


def get_note_list() -> list:
    def search_all_notes(cur_path: str, indent: int = 0, dir_list=[]):
        prev_item = ""

        for item in sorted(os.listdir(cur_path)):
            if "{}.{}".format(prev_item, config.get("extension")) == item:
                continue
            if os.path.isdir(os.path.join(cur_path, item)) and "{}.{}".format(
                item, config.get("extension")
            ) in os.listdir(cur_path):
                # Note with subfolder
                dir_list.append(
                    Note(
                        os.path.join(cur_path, f"{item}.{config.get('extension')}"),
                        indent=indent,
                    )
                )
            elif item.endswith(config.get("markdown_extensions")):
                # Note Only
                dir_list.append(Note(os.path.join(cur_path, item), indent=indent))

            if os.path.isdir(os.path.join(cur_path, item)):
                search_all_notes(
                    os.path.join(cur_path, item), indent=indent + 1, dir_list=dir_list
                )
            prev_item = item
        return dir_list

    notes = []
    for note_path in config.get("note_paths"):
        notes.extend(search_all_notes(note_path, dir_list=[]))

    count = 1
    for note in notes:
        note.count_id = count
        count += 1
    return notes


def view_note(view_note: str):
    if os.path.isfile(view_note):
        relevent_notes = [Note(view_note)]
    else:
        relevent_notes = search_note_by_name(view_note)
    found_note = None

    if not relevent_notes:
        print(f"No matching note called or containing: {view_note}")
        deep_search_within_note(view_note)
    else:
        found_note = note_selection(relevent_notes)

    if found_note:
        MarkdownParse(found_note).print()


def search_note_by_name(name: str, notes: List[Note] = None) -> list:
    if not notes:
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
    if len(note_list) == 0:
        print("No relevent Notes")
    for note in note_list:

        print(
            f"{fontColor(Color.GREY, bright = True, style = Style.ITALIC)} ({note.count_id}){fontReset()}",
            end="\t",
        )
        print(
            " " + f"- {fontColor()}{remove_suffix(note.min_path)}{fontReset()}",
        )

        if list_contents:
            for content in note.contents:
                print(
                    "  " * content.indent
                    + f"{fontColor(setcolor = Color.YELLOW)}{content.title}{fontReset()}"
                )
        if note.extra_info:
            for line in note.extra_info:
                print(
                    "-------------------\n"
                    + f"{fontColor(setcolor = Color.RED)}{line}{fontReset()}"
                )


def add_note(note_name: str, note_msg: str = "", no_edit=False):
    title = note_name

    if title.split(".")[-1] in config.get("markdown_extensions"):
        title = os.path.join(*title.split(".")[:-1])

    title = title.replace(".", "/")

    note = Note(
        os.path.join(
            config.get("primary_note_dir"), f"{title}.{config.get('extension')}"
        )
    )

    if os.path.exists(os.path.dirname(note.path)) is False:
        if confirm_choice(f"Create note path {os.path.dirname(note.path)}?"):
            os.makedirs(os.path.dirname(note.path))
        else:
            return

    if os.path.isfile(note.path) is False:
        with open(note.path, "w") as note_file:
            note_file.write(f"# {note.name}\n{note_msg}")
    else:
        print("Note already exists, editing")
    if not note_msg and not no_edit:
        call(f"{config.get('editor')} {note.path}", shell=True)


def edit_note(edit_note: str):
    relevent_notes = search_note_by_name(edit_note)

    note = note_selection(relevent_notes)

    call(f"{config.get('editor')} {note.path}", shell=True)


def delete_note(rm_note: str, confirm: bool = True):
    relevent_notes = search_note_by_name(rm_note)
    if not relevent_notes:
        print(f"No matches")
        return

    choice = note_selection(relevent_notes)

    if (choice and not confirm) or (
        choice and confirm_choice("Do you wish to delete {}".format(choice.min_path))
    ):
        try:
            os.remove(choice.path)
            print(f"Deleted {choice.min_path}")
        except:
            print("Could not delete")
    else:
        print(f"Not deleting: {choice.min_path}")
        return


def search_note(search_note: str, list_contents=False):
    relevent_notes = search_note_by_name(search_note)
    list_notes(relevent_notes, list_contents=list_contents)


def deep_search_for_text(text: str) -> List[Note]:
    return [note for note in get_note_list() if note.text_search(text)]


def deep_search_within_note(search_text: str, search_note_name: str = None):
    if search_note_name:
        list_notes(
            search_note_by_name(search_note_name, deep_search_for_text(search_text))
        )
    else:
        list_notes(deep_search_for_text(search_text))


def configure_config():
    call(f"{config.get('editor')} {config.config_path}", shell=True)


def parse_args() -> dict:
    argument_options = ["view", "add", "rm", "edit", "ds", "ls", "config"]

    # Argparse cant allow optional positional arguments with sub parser
    # this hack pretends to be view argument for quick views
    if len(sys.argv) == 2 and sys.argv[1] not in argument_options:
        return SimpleNamespace(view=True, substring=sys.argv[1])
    elif len(sys.argv) < 2:
        return SimpleNamespace(list=True, contents=False, substring="")

    arguments = argparse.ArgumentParser(
        description="Notes. Simple cli tool for creating and managing markdown notes."
    )

    arguments.add_argument(
        "--version", action="version", version=f"%(prog)s {_version}"
    )

    subparsers = arguments.add_subparsers(help="Action sub-command help")

    # View
    viewParser = subparsers.add_parser("view", help="View Note")
    viewParser.add_argument("-v", dest="view", default=True, help=argparse.SUPPRESS)
    viewParser.add_argument("substring", type=str, help="Note name/substring")

    # Add
    addNoteparser = subparsers.add_parser("add", help="Add new Notes")
    addNoteparser.add_argument("-n", dest="add", default=True, help=argparse.SUPPRESS)
    addNoteparser.add_argument("note_name", type=str, help="New Note Name")
    addNoteparser.add_argument(
        "note_text", type=str, default="", help="Quickly add Note text"
    )

    # Edit
    addNoteparser = subparsers.add_parser("edit", help="Edit Notes")
    addNoteparser.add_argument("-n", dest="edit", default=True, help=argparse.SUPPRESS)
    addNoteparser.add_argument("note_name", type=str, help="Note Name")

    # Delete
    deleteParser = subparsers.add_parser("rm", help="Delete Note")
    deleteParser.add_argument(
        "-rm", dest="delete", default=True, help=argparse.SUPPRESS
    )
    deleteParser.add_argument("note_name", type=str, help="Note name/substring")

    # List
    listparser = subparsers.add_parser("ls", help="List Notes")
    listparser.add_argument("-ls", dest="list", default=True, help=argparse.SUPPRESS)
    listparser.add_argument(
        "substring", type=str, nargs="?", default="", help="search title substring"
    )
    listparser.add_argument(
        "-c",
        "--list-contents",
        dest="contents",
        action="store_true",
        default=False,
        help="List the contents of Notes",
    )

    # Deepsearch
    deepSearchParser = subparsers.add_parser("ds", help="Search in Notes")
    deepSearchParser.add_argument(
        "-ds", dest="dsearch", default=True, help=argparse.SUPPRESS
    )
    deepSearchParser.add_argument("substring", type=str, help="search substring")
    deepSearchParser.add_argument(
        "note_name",
        type=str,
        nargs="?",
        default="",
        help="Notes to search substring within",
    )

    # Config
    configParser = subparsers.add_parser("config", help="Change config file")
    configParser.add_argument(
        "-cfg", dest="config", default=True, help=argparse.SUPPRESS
    )

    args = arguments.parse_args()

    return args


def main():
    arguments = parse_args()

    if hasattr(arguments, "add"):
        add_note(arguments.note_name, arguments.note_text)
    elif hasattr(arguments, "edit"):
        edit_note(arguments.note_name)
    elif hasattr(arguments, "list"):
        search_note(arguments.substring, list_contents=arguments.contents)
    elif hasattr(arguments, "delete"):
        delete_note(arguments.note_name)
    elif hasattr(arguments, "dsearch"):
        deep_search_within_note(arguments.substring, arguments.note_name)
    elif hasattr(arguments, "view"):
        view_note(arguments.substring)
    elif hasattr(arguments, "config"):
        configure_config()


if __name__ == "__main__":
    main()
