# CLI Notes
Simple cli note tool and organiser. Using Markdown for human readable and easily creatable note files.

## Usage
mknotes NOTE_name                      Outputs the notes

### Options
    -a | --alter        <name>  Add/Alter a new note
    -d | --delete       <name>  Deletes notes
    -l | --list                 List the notes
    -ll| --sub-list             List notes and their table of contents
    -s | --search       <text>  Search notes for text in a title.
    -ds| --deep-search  <text>  deepsearch notes, searches string of text in title's and contents of notes.

    -c | --config               Alter the configurations for CLI notes
    -h | --help                 The help menu


## Features

### Features
 - Add, Edit, Delete Notes
 - Notes are plaintext markdown with extending subfolders
 - List notes, all or from subfolder
 - extended notes list, list notes and their contents, all or from subfolders
 - Search notes, regex either by note name or it's contents, list all matches
    outputs if single match

### Wishlist
 - Markdown color customisation (Should be easy with MDV)
 - Delete by folder
 - Configure option to allow single config change rather the open file
 - notes links to other notes, local or separated
 - Dynamic notes (runs commands to import into note, E.G "ls", "ip a", etc
 - Flat pack notes? (compress)
 - Interactive mode
    ''-i | --interactive          Interactive mode, uses Less to display rather then dump''
