"""
Help text for Suplemon
"""

help_text = """
# Suplemon Help

*Contents*
1. General description
2. User interface
3. Default keyboard shortcuts
4. Commands

## 1. General description
Suplemon is designed to be an easy, intuitive and powerful text editor.
It emulates some features from Sublime Text and the user interface of Nano.
Multi cursor editing is a core feature. Suplemon also supports extensions
so you can customize it to work how you want.

## 2. User interface
The user interface is designed to be as intuitive and informative as possible.
There are two status bars, one at the top and one at the bottom. The top bar
shows the program version, a clock, and a list of opened files. The bottom bar
shows status messages and handles input for commands. Above the bottom status
bar there is a list of most common keyboard shortcuts.

## 3. Default keyboard shortcuts
The default keyboard shortcuts imitate those of common graphical editors.
Most shortcuts are also shown at the bottom in the legend area. Here's
the complete reference.


 * Ctrl + Q
   > Exit

 * Ctrl + W
   > Close file or tab

 * Ctrl + C
   > Copy line(s) to buffer

 * Ctrl + X
   > Cut line(s) to buffer

 * Ctrl + V
   > Insert buffer

 * Ctrl + K
   > Duplicate line

 * Ctrl + G
   > Go to line number or file (type the beginning of a filename to switch to it).
   > You can also use 'filena:42' to go to line 42 in filename.py etc.

 * Ctrl + F
   > Search for a string or regular expression (configurable)

 * Ctrl + D
   > Search for next occurance or find the word the cursor is on. Adds a new cursor at each new occurance.

 * Ctrl + T
   > Trim whitespace

 * Alt + Arrow Key
   > Add new curor in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word or line

 * ESC
   > Revert to a single cursor / Cancel input prompt

 * Alt + Page Up
   > Move line(s) up

 * Alt + Page Down
   > Move line(s) down

 * Ctrl + S
   > Save current file

 * F1
   > Save file with new name

 * F2
   > Reload current file

 * Ctrl + O
   > Open file

 * Ctrl + W
   > Close file

 * Ctrl + Page Up
   > Switch to next file

 * Ctrl + Page Down
   > Switch to previous file

 * Ctrl + E
   > Run a command.

 * F5
   > Undo

 * F6
   > Redo

 * F7
   > Toggle visible whitespace

 * F8
   > Toggle mouse mode

 * F9
   > Toggle line numbers

 * F11
   > Toggle full screen

### Mouse shortcuts

 * Left Click
   > Set cursor at mouse position. Reverts to a single cursor.

 * Right Click
   > Add a cursor at mouse position.

 * Scroll Wheel Up / Down
   > Scroll up & down.


## 4. Commands
Commands are special operations that can be performed (e.g. remove whitespace
or convert line to uppercase). Each command can be run by pressing Ctrl + E
and then typing the command name. Commands are extensions and are stored in
the modules folder in the Suplemon installation.

 * autocomplete

    A simple autocompletion module.

    This adds autocomplete support for the tab key. It uses a word
    list scanned from all open files for completions. By default it suggests
    the shortest possible match. If there are no matches, the tab action is
    run normally.

 * autodocstring

    Simple module for adding docstring placeholders.

    This module is intended to generate docstrings for Python functions.
    It adds placeholders for descriptions, arguments and return data.
    Function arguments are crudely parsed from the function definition
    and return statements are scanned from the function body.

 * bulk_delete

    Bulk delete lines and characters.
    Asks what direction to delete in by default.

    Add 'up' to delete lines above highest cursor.
    Add 'down' to delete lines below lowest cursor.
    Add 'left' to delete characters to the left of all cursors.
    Add 'right' to delete characters to the right of all cursors.

 * comment

    Toggle line commenting based on current file syntax.

 * config

    Shortcut for openning the config files.

 * crypt

    Encrypt or decrypt the current buffer. Lets you provide a passphrase and optional salt for encryption.
    Uses AES for encryption and scrypt for key generation.

 * diff

    View a diff of the current file compared to it's on disk version.

 * eval

    Evaluate a python expression and show the result in the status bar.

    If no expression is provided the current line(s) are evaluated and
    replaced with the evaluation result.

 * keymap

    Shortcut to openning the keymap config file.

 * linter

    Linter for suplemon.

 * lower

    Transform current lines to lower case.

 * lstrip

    Trim whitespace from beginning of current lines.

 * paste

    Toggle paste mode (helpful when pasting over SSH if auto indent is enabled)

 * reload

    Reload all add-on modules.

 * replace_all

    Replace all occurrences in all files of given text with given replacement.

 * reverse

    Reverse text on current line(s).

 * rstrip

    Trim whitespace from the end of lines.

 * save

    Save the current file.

 * save_all

    Save all currently open files. Asks for confirmation.

 * sort_lines

    Sort current lines.

    Sorts alphabetically by default.
    Add 'length' to sort by length.
    Add 'reverse' to reverse the sorting.

 * strip

    Trim whitespace from start and end of lines.

 * tabstospaces

    Convert tab characters to spaces in the entire file.

 * toggle_whitespace

    Toggle visually showing whitespace.

 * upper

    Transform current lines to upper case.


"""
