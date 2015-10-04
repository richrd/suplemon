Suplemon :lemon: [![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=master)](https://travis-ci.org/richrd/suplemon)
========
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

## Suplemon multi cursor editing
![Suplemon in action](http://bittemple.org/misc/suplemon/suplemon-demo.gif)


## Get it!
You can just clone the repo, and try Suplemon, or also install it system wide.

    git clone https://github.com/richrd/suplemon.git
    cd suplemon
    python3 suplemon.py

### Installation
To install Suplemon run the setup script:

    sudo python3 setup.py install

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

 * xsel
 > For system clipboard support on X Window (Linux).

 See [docs/optional-dependencies.md][] for installation instructions.

 [docs/optional-dependencies.md]: docs/optional-dependencies.md

## Usage

    suplemon # New file in the current directory
    suplemon [filename]... # Open one or more files

## Description
Suplemon is an intuitive command line text editor. It supports multiple cursors out of the box.
It is as easy as nano, and has much of the power of Sublime Text. It also supports extensions
to allow all kinds of customizations. To get more help hit ```Ctrl + H``` in the editor.
Suplemon is licensed under the MIT license.

## Features
 * Terminal text editing with style
 * Proper multi cursor editing, Sublime Text style.
 * Syntax highlighting
 * Autocomplete
 * Easy Undo/Redo
 * Copy & Paste, with multi line support (and native clipboard support on X11 / Unix)
 * Multiple files in tabs
 * Powerful Go To feature for jumping to files and lines
 * Find and Find next
 * Custom keyboard shortcuts
 * Mouse support
 * Extensions (easy to write your own)
 * Lots more...

## Goals
 1. [X] Create a command line text editor with built in multi cursor support. It's awesome!
 2. [X] Usability should be even better and easier than nano. It's on par with desktop editors.
 3. [X] Multi cursor should be comparable to Sublime Text.
 4. [X] Develop Suplemon with Suplemon!!! I've used Suplemon for a long time as my main
        editor (replacing ST and nano) for all developement, Git commits and everything else.

## Configuration

The suplemon config file is stored at ```~/.config/suplemon/suplemon-config.json```.

The best way to edit it is to run the ```config``` command (Run commands via ```Ctrl+E```).
That way Suplemon will automatically reload the configuration when you save the file.
You can find all the configuration options and descriptions in the suplemon/config.py file.


## Keyboard shortcuts

 * Ctrl + Q
   > Exit

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
   > Search for next occurrence or find the word the cursor is on. Adds a new cursor at each new occurrence.

 * Alt + Arrow Key
   > Add new cursor in arrow direction

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

## Mouse shortcuts

 * Left Click
   > Set cursor at mouse position. Reverts to a single cursor.

 * Right Click
   > Add a cursor at mouse position.

 * Scroll Wheel Up / Down
   > Scroll up & down.


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

## Todo
 * [ ] Remember cursor positions in files (and restore when opened again)
 * [ ] Design proper API for plugins/extensions/macros
 * [ ] Documentation for v 1.0.0
 * [ ] Package Suplemon and upload to PIP

## Wishlist (Stuff that would be nice, but not planning to do yet. *Maybe* for 2.0.0)
 * [X] Display tab characters with a replacement char (tab messes up lines)
 * [X] Global clipboard (copy from one file to another)
 * [ ] Core
   * [ ] Optimize rendering for ssh (minimal screen update)
   * [ ] Setting for enabling/disabling undo for cursor changes
   * [ ] Selections
   * [ ] List of recent files
   * [ ] Read only viewer
      * ~~And disable editing~~ Don't disable editing. Instead enable save as.
   * [ ] Only refresh cursors when moving around
   * [ ] Only refresh modified lines when editing
 * [ ] Extensions:
   * [ ] Peer to peer colaborative editing. Could be implemented as an extension.
   * [ ] Auto backup. Activate on n changes or every n seconds
   * [ ] File selector, kind of like what nano has
     * [ ] This should be implemented as an extension
     * [ ] Could be triggered with a key binding (and/or override open file)
     * [ ] Need to refactor App class to support views instead of just files
     * [ ] A view could be an editor or an extension ui
     * [ ] Extensions should be able to control both status bars and key legend
   * [ ] Automatically add ; to end of lines
      * [ ] Generalized: add line prepend and append commands
      * [ ] Will need multiline comment and string detection etc.

## Fix / Defects
 * [ ] Input queries can't detect trailing whitespace
 * [ ] Remember find query if occurance not found (jump to top of file)


## Rationale
For many the command line is a different environment for text editing.
Most coders are familiar with GUI text editors and for many vi and emacs
have a too steep learning curve. For them (like for me) nano was the weapon of
choice. But nano feels clunky and it has its limitations. That's why
I wrote my own editor with built in multi cursor support to fix the situation.
Another reason is that developing Suplemon is simply fun to do.
