Suplemon :lemon:
========

[![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=master)](https://travis-ci.org/richrd/suplemon) [![Join the chat at https://webchat.freenode.net/?channels=%23suplemon](https://img.shields.io/badge/chat-on%20freenode%20%23suplemon-blue.svg)](https://webchat.freenode.net/?channels=%23suplemon)

          ___________   _________  ___     ______________________________   ___
         /  _____/  /  /  /  _   \/  /\   /  ______/        /  ___   /   | /  /\
        /  /____/  /  /  /  /_/  /  / /  /  /_____/  /  /  /  /  /  /    |/  / /
       /____   /  /  /  /  _____/  / /  /  ______/  /  /  /  /  /  /  /|    / /
      _____/  /  /__/  /  /\___/  /____/  /_____/  /  /  /  /__/  /  / |   / /
     /_______/\_______/__/ /  /_______/________/__/__/__/________/__/ /|__/ /
     \_______\ \______\__\/   \_______\________\__\__\__\________\__\/ \__\/

              Remedying the pain of command line editing since 2014


Suplemon is a modern, powerful and intuitive console text editor with multi cursor support.
Suplemon replicates Sublime Text style functionality in the terminal with the ease of use of Nano.
http://github.com/richrd/suplemon

![Suplemon in action](http://bittemple.org/sites/suplemon.com/assets/suplemon-v0.1.51-multi-cursor-editing.gif)

## Features
 * Proper multi cursor editing, as in Sublime Text
 * Syntax highlighting with Text Mate themes
 * Autocomplete (based on words in the files that are open)
 * Easy Undo/Redo (Ctrl + Z, Ctrl + Y)
 * Copy & Paste, with multi line support (and native clipboard support on X11 / Unix and Mac OS)
 * Multiple files in tabs
 * Powerful Go To feature for jumping to files and lines
 * Find, Find next and Find all (Ctrl + F, Ctrl + D, Ctrl + A)
 * Custom keyboard shortcuts (and easy-to-use defaults)
 * Mouse support
 * Restores cursor and scroll positions when reopenning files
 * Extensions (easy to write your own)
 * Lots more...


## Caveats
 * Currently no built in selections (regions). To copy part of a line select it with your mouse and use <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd>

## Try it!

You can just clone the repo, and try Suplemon, or also install it system wide.
To run from source you need to install the python `wcwidth` package.

    pip3 install wcwidth
    git clone https://github.com/richrd/suplemon.git
    cd suplemon
    python3 suplemon.py

### Installation

Install the latest version from PIP:

    sudo pip3 install suplemon

To install Suplemon from the repo run the setup script:

    sudo python3 setup.py install

### Usage

    suplemon # New file in the current directory
    suplemon [filename]... # Open one or more files


### Notes
 - **Must use Python 3.3 or higher for proper character encoding support.**
 - **Python2.7 (and maybe lower) versions work, but aren't officially supported (some special characters won't work etc).**
 - *The master branch is considered stable.*
 - *Tested on Unix.*

Dev Branch Status: [![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=dev)](https://travis-ci.org/richrd/suplemon)

No dependencies outside the Python Standard Library required.

### Optional dependencies

 * Pygments
 > For support for syntax highlighting over 300 languages.

 * Flake8
 > For showing linting for Python files.

 * xsel or xclip
 > For system clipboard support on X Window (Linux).

 * pbcopy / pbpaste
 > For system clipboard support on Mac OS.

 See [docs/optional-dependencies.md][] for installation instructions.

 [docs/optional-dependencies.md]: docs/optional-dependencies.md

## Description
Suplemon is an intuitive command line text editor. It supports multiple cursors out of the box.
It is as easy as nano, and has much of the power of Sublime Text. It also supports extensions
to allow all kinds of customizations. To get more help hit ```Ctrl + H``` in the editor.
Suplemon is licensed under the MIT license.

## Configuration

### Main Config
The suplemon config file is stored at ```~/.config/suplemon/suplemon-config.json```.

The best way to edit it is to run the ```config``` command (Run commands via ```Ctrl+E```).
That way Suplemon will automatically reload the configuration when you save the file.
To view the default configuration and see what options are available run ```config defaults``` via ```Ctrl+E```.


### Keymap Config

Below are the default key mappings used in suplemon. They can be edited by running the ```keymap``` command.
To view the default keymap file run ```keymap default```

 * <kbd>Ctrl</kbd> + <kbd>Q</kbd>
   > Exit

 * <kbd>Ctrl</kbd> + <kbd>W</kbd>
   > Close file or tab

 * <kbd>Ctrl</kbd> + <kbd>C</kbd>
   > Copy line(s) to buffer

 * <kbd>Ctrl</kbd> + <kbd>X</kbd>
   > Cut line(s) to buffer

 * <kbd>Ctrl</kbd> + <kbd>V</kbd>
   > Insert buffer

 * <kbd>Ctrl</kbd> + <kbd>K</kbd>
   > Duplicate line

 * <kbd>Ctrl</kbd> + <kbd>G</kbd>
   > Go to line number or file (type the beginning of a filename to switch to it).
   > You can also use 'filena:42' to go to line 42 in filename.py etc.

 * <kbd>Ctrl</kbd> + <kbd>F</kbd>
   > Search for a string or regular expression (configurable)

 * <kbd>Ctrl</kbd> + <kbd>D</kbd>
   > Search for next occurrence or find the word the cursor is on. Adds a new cursor at each new occurrence.

 * <kbd>Ctrl</kbd> + <kbd>T</kbd>
   > Trim whitespace

 * <kbd>Alt</kbd> + <kbd>Arrow Key</kbd>
   > Add new cursor in arrow direction

 * <kbd>Ctrl</kbd> + <kbd>Left / Right</kbd>
   > Jump to previous or next word or line

 * <kbd>ESC</kbd>
   > Revert to a single cursor / Cancel input prompt

 * <kbd>Alt</kbd> + <kbd>Page Up</kbd>
   > Move line(s) up

 * <kbd>Alt</kbd> + <kbd>Page Down</kbd>
   > Move line(s) down

 * <kbd>Ctrl</kbd> + <kbd>S</kbd>
   > Save current file

 * <kbd>F1</kbd>
   > Save file with new name

 * <kbd>F2</kbd>
   > Reload current file

 * <kbd>Ctrl</kbd> + <kbd>O</kbd>
   > Open file

 * <kbd>Ctrl</kbd> + <kbd>W</kbd>
   > Close file

 * <kbd>Ctrl</kbd> + <kbd>Page Up</kbd>
   > Switch to next file

 * <kbd>Ctrl</kbd> + <kbd>Page Down</kbd>
   > Switch to previous file

 * <kbd>Ctrl</kbd> + <kbd>E</kbd>
   > Run a command.

 * <kbd>Ctrl</kbd> + <kbd>Z</kbd> and <kbd>F5</kbd>
   > Undo

 * <kbd>Ctrl</kbd> + <kbd>Y</kbd> and <kbd>F6</kbd>
   > Redo

 * <kbd>F7</kbd>
   > Toggle visible whitespace

 * <kbd>F8</kbd>
   > Toggle mouse mode

 * <kbd>F9</kbd>
   > Toggle line numbers

 * <kbd>F11</kbd>
   > Toggle full screen

## Mouse shortcuts

 * Left Click
   > Set cursor at mouse position. Reverts to a single cursor.

 * Right Click
   > Add a cursor at mouse position.

 * Scroll Wheel Up / Down
   > Scroll up & down.

## Commands

Suplemon has various add-ons that implement extra features.
The commands can be run with <kbd>Ctrl</kbd> + <kbd>E</kbd> and the prompt has autocomplete to make running them faster.
The available commands and their descriptions are:

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


## Support

If you experience problems, please submit a new issue.
If you have a question, need help, or just want to chat head over to the IRC channel #suplemon @ Freenode.
I'll be happy to chat with you, see you there!


## Development

If you are interested in contributing to Suplemon, development dependencies can be installed via:

    # For OS cleanliness, we recommend using `virtualenv` to prevent global contamination
    pip install -r requirements-dev.txt

After those are installed, tests can be run via:

    ./test.sh

PRs are very welcome and appreciated.
When making PRs make sure to set the target branch to `dev`. I only push to master when releasing new versions.


## Rationale
For many the command line is a different environment for text editing.
Most coders are familiar with GUI text editors and for many vi and emacs
have a too steep learning curve. For them (like for me) nano was the weapon of
choice. But nano feels clunky and it has its limitations. That's why
I wrote my own editor with built in multi cursor support to fix the situation.
Another reason is that developing Suplemon is simply fun to do.
