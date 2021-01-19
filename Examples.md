# Notes Usage Examples
Notes offers basic arguments which also work positional to speed up workflow, this file contains examples for key features.

## Options
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

## Creating/Editing Note
```
$ notes -a bullet
 - bullet
...
```

## Listing notes
```
$ notes 
 (1)	 - bullet.README
 (2)	 - magnetToTorrent.README
 (3)	 - notes.README
 (4)	 - pitopexercise.README
 (5)	 - ttcnotify.README
 (6)	 - ytalbumdl.README
```
```
$ notes -l
 (1)	 - bullet.README
 (2)	 - magnetToTorrent.README
 (3)	 - notes.README
 (4)	 - pitopexercise.README
 (5)	 - ttcnotify.README
 (6)	 - ytalbumdl.README
```

## Reading notes
```
$ notes bullet
bullet.README
...
```
```
$ notes 1
bullet.README
...
```

## Searching notes
Searching notes is done automatically when no known title is given
### Search by Title
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
### Searching by Content
```
$ notes this
No matching note called: this
 (17)    - ttcnotify.README
    32:   -h, --help            show this help message and exit
    36: The simple script requires a URL to alter, for this initially search TTC for the item. Copy the URL into the
```

