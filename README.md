# CLI Notes
Notes is a simple CLI tool for Creating, Reading and managing personal notes using Markdown.
The tool holds it's own directory of Markdown Notes which is used by default, multiple paths can be given
including a workspace containing Markdown README files.
Relies upon [terminal markdown viewer (MDV)](https://github.com/axiros/terminal_markdown_viewer) to parse and output
the Markdown.

## Features
 - Add, Edit, Delete Notes
 - Notes are plaintext markdown with extending subfolders
 - List notes, all or from subfolder
 - extended notes list, list notes and their contents, all or from subfolders
 - Search notes, regex either by note name or it's contents, list all matches
    outputs if single match

## Usage
Full examples of usage can be seen [here](Examples.md)

### Options
    <text>                      Positional argument, a note name or text within a note
    -a | --alter        <name>  Add/Alter a new note
        --dir        <name>     Optional argument to  create a project directory then a note
    -d | --delete       <name>  Deletes notes
    -l | --list                 List the notes (Default action)
    -ll| --sub-list             List notes and their table of contents
    -s | --search       <text>  Search notes for text in a title.
    -ds| --deep-search  <text>  deepsearch notes, searches string of text in title's and contents of notes.

    -c | --config               Alter the configurations for CLI notes
    -h | --help                 The help menu


## Installation
Notes requires `python3` for installation and can be installed via:
```
$ pip3 install .
```

### Requirements
Only requirement being [MDV](https://github.com/axiros/terminal_markdown_viewer)
```
$ pip3 install -R requirements.txt
```

## Dev Running
To run the script from git clone, locally use:
```
$ python3 -m notes.notes
```

## ToDo
 - Pip Packaged (Correctly)
 - Unit Tests
 - search by Shiet note ID 
 - Ability to delete dir

### Wishlist
 - Markdown color customisation (Should be easy with MDV)
 - Dynamic notes (runs commands to import into note, E.G "ls", "ip a", etc
 - Configure option to allow single config change rather the open file
 - notes links to other notes - Maybe possible with MDV changes or swiching to MAN pages
 - Flat pack notes? (compress)
