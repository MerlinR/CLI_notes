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
### Options
    <text>                      Positional argument, a note name or text within a note
    -a | --alter        <name>  Add/Alter a new note
    -d | --delete       <name>  Deletes notes
    -l | --list                 List the notes (Default action)
    -ll| --sub-list             List notes and their table of contents
    -s | --search       <text>  Search notes for text in a title.
    -ds| --deep-search  <text>  deepsearch notes, searches string of text in title's and contents of notes.

    -c | --config               Alter the configurations for CLI notes
    -h | --help                 The help menu

### Creating/Editing Note
```
$ notes -a bullet
 - bullet.README
...
```

### Listing notes
```
$ notes 
 (1)	 - bullet.README
 (2)	 - magnetToTorrent.README
 (3)	 - notes.README
 (4)	 - pitopexercise.README
 (5)	 - ttcnotify.README
 (6)	 - yt_album_dl.README
```

### Reading notes
```
$ notes bullet
bullet.README
...
```

### Searching notes
```
$ notes this
No matching note called: this
 (17)    - ttcnotify.README
    32:   -h, --help            show this help message and exit
    36: The simple script requires a URL to alter, for this initially search TTC for the item. Copy the URL into the
```

```
$ notes a
 (1)	 - a
 (2)	 - a.1
 (3)	 - a.2
 (4)	 - a2
 (14)	 - magnetToTorrent.README
 (18)	 - yt_album_dl.README
Please select a note: [1, 2, 3, 4, 14, 18]
Note selection or [q]uit:
```

## Installation

### Requirements
Only requirement being [MDV](https://github.com/axiros/terminal_markdown_viewer)
```
$ pip install -R requirements.txt
```

## ToDo
 - Pip Packaged
 - Unit Tests
 - search by Shiet note ID 
 - 
### Wishlist
 - Markdown color customisation (Should be easy with MDV)
 - Delete by folder
 - notes links to other notes
 - Dynamic notes (runs commands to import into note, E.G "ls", "ip a", etc
 - Configure option to allow single config change rather the open file
 - Flat pack notes? (compress)
 - Interactive mode
    ''-i | --interactive          Interactive mode, uses Less to display rather then dump''
