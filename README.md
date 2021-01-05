# CLI Notes
Simple cli note tool and orgniser. Using Markdown for human readable and easily createable note files.

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
 - exteneded notes list, list notes and their contents, all or from subfolders
 - Search notes, regex either by note name or it's contents, list all matches
    outputs if single match

### Wishlist
 - Search for project, lists notes in folder
 - multiple note Dir's for code README's
 - notes links to other notes, local or seperaterd
 - Dynamic notes (runs commands to import into note, E.G "ls", "ip a", etc
 - Interactive mode
    ''-i | --interactive          Interactive mode, uses Less to display rather then dump''
