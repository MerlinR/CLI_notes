#!/usr/bin/python3
import argparse
import os
import re
import sys
from pathlib import Path
from subprocess import call
from typing import Optional

from notes.lib.definitions import Note
from notes.lib.misc import Color, Style, fontColor, fontReset
from notes.lib.parseMarkdown import MarkdownParse
from notes.lib.settings import config


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
    # Easier way to get all MD files, although order is not as pleased
    # result = list(Path(config["note_paths"][0]).rglob(f"*.{config['extension']}"))
    # for found in sorted(result):
    #    notes.append(Note(str(found)))

    count = 1
    for note in notes:
        note.count_id = count
        note.contents = get_note_contents(note.path)
        count += 1
    return notes


def view_note(view_note: str):
    if os.path.isfile(view_note):
        relevent_notes = [Note(view_not)]
    else:
        relevent_notes = search_note_by_name(view_note)
    found_note = None
    if not relevent_notes:
        print(f"No matching note called or containing: {view_note}")
        deep_search_within_note(view_note)
    elif len(relevent_notes) == 1:
        found_note = relevent_notes[0]
    else:
        list_notes(relevent_notes)
        options = [note.count_id for note in relevent_notes]
        choice = note_selection(f"Please select a note: {options}", options)

        found_note = [note for note in relevent_notes if note.count_id == choice][0]

    if found_note:
        MarkdownParse(found_note).print()


def search_note_by_name(name: str) -> list:
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

    for note in note_list:
        note_name = os.path.basename(note.path)
        note_indent = note.indent

        print(
            f"{fontColor(Color.GREY, bright = True, style = Style.ITALIC)} ({note.count_id}){fontReset()}",
            end="\t",
        )
        print(
            " " + f"- {fontColor()}{remove_suffix(note.min_path)}{fontReset()}",
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


def alter_note(alter_note: str, createDir=None):
    title = alter_note
    if title.split(".")[-1] in config.get("markdown_extensions"):
        title = os.path.join(*title.split(".")[:-1])

    title = title.replace(".", "/")

    note = Note(
        os.path.join(
            config.get("primary_note_dir"), f"{title}.{config.get('extension')}"
        )
    )

    if createDir:
        newPath = f"{remove_suffix(note.path)}"
        if os.path.exists(newPath) is False:
            os.makedirs(newPath)
        return
    elif os.path.exists(os.path.dirname(note.path)) is False:
        if confirm_choice(f"Create note path {os.path.dirname(note.path)}?"):
            os.makedirs(os.path.dirname(note.path))
        else:
            return

    if os.path.isfile(note.path) is False:
        with open(note.path, "w") as note_file:
            note_file.write("#{}\n".format(note.name))

    call(f"{config.get('editor')} {note.path}", shell=True)


def configure_config(configure: str):
    call(f"{config.get('editor')} {config.config_path}", shell=True)


def delete_note(rm_note: str, deleteDir=None):
    relevent_notes = search_note_by_name(rm_note)
    choice = False

    if len(relevent_notes) > 1:
        list_notes(relevent_notes)
        options = [note.count_id for note in relevent_notes]
        choice = note_selection(f"Please select a note: {options}", options)
    elif confirm_choice("Do you wish to delete {}".format(relevent_notes[0].min_path)):
        choice = relevent_notes[0].count_id
    elif not choice:
        print(f"Not deleting: {rm_note}")
        return

    note = [note for note in relevent_notes if note.count_id == choice][0]
    try:
        os.remove(note.path)
        print(f"Deleted {note.min_path}")
    except:
        print("Could not delete")


def search_note(search_note: str):
    relevent_notes = search_note_by_name(search_note)
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
        description="Notes. Simple cli tool for creating and managing markdown notes."
    )

    arguments.add_argument(
        dest="view", nargs="?", type=str, help="View specific note, will do a search"
    )

    arguments.add_argument(
        "-a", "--alter", dest="alter", type=str, help="Add/Edit note"
    )

    arguments.add_argument(
        "--dir",
        dest="dirOption",
        action="store_true",
        default=None,
        help="creates directory as a project rather then MD file",
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

    if args.dirOption and (args.alter is None and args.delete is None):
        print("--dir only used in conjuction with --alter to create a project dir")
        sys.exit()
    if len(sys.argv) < 2:
        args.list = True

    return args


def main():
    arguments = parse_args()

    if arguments.view:
        view_note(arguments.view)
    elif arguments.alter:
        alter_note(arguments.alter, arguments.dirOption)
    elif arguments.delete:
        delete_note(arguments.delete, arguments.dirOption)
    elif arguments.list:
        list_notes(get_note_list())
    elif arguments.sublist:
        list_notes(get_note_list(), list_contents=True)
    elif arguments.search:
        search_note(arguments.search)
    elif arguments.dsearch:
        deep_search_within_note(arguments.dsearch)
    elif arguments.configure:
        configure_config(arguments.configure)


if __name__ == "__main__":
    main()
