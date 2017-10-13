Suplemon :lemon:
========

[![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=master)](https://travis-ci.org/richrd/suplemon) [![Join the chat at https://gitter.im/richrd/suplemon](https://badges.gitter.im/richrd/suplemon.svg)](https://gitter.im/richrd/suplemon?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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
 * Restores cursor positions in when reopenning files
 * Extensions (easy to write your own)
 * Lots more...


## Caveats
 * Currently no built in selections (regions). To copy part of a line select it with your mouse and use <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd>

## Try it!

You can just clone the repo, and try Suplemon, or also install it system wide.

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

 * xsel
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

## Goals
 1. [X] Create a command line text editor with built in multi cursor support. It's awesome!
 2. [X] Usability should be even better and easier than nano. It's on par with desktop editors.
 3. [X] Multi cursor should be comparable to Sublime Text.
 4. [X] Develop Suplemon with Suplemon!!! I've used Suplemon for a long time as my main
        editor (replacing ST and nano) for all developement, Git commits and everything else.

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


## Todo
 * [ ] Design proper API for plugins/extensions/macros
 * [ ] Documentation for v 1.0.0

## Wishlist (Stuff that would be nice, but not planning to do yet. *Maybe* for 2.0.0)
 * [ ] Core
   * [ ] Setting for enabling/disabling undo for cursor changes
   * [ ] Selections
   * [ ] List of recent files
   * [X] Optionally Remember cursor positions in files (and restore when opened again)
   * [ ] Read only viewer
      * ~~And disable editing~~ Don't disable editing. Instead enable save as.
 * [ ] Extensions:
   * [ ] Peer to peer colaborative editing. Could be implemented as an extension.
   * [ ] Auto backup. Activate on n changes or every n seconds
   * [ ] File selector, kind of like what nano has
     * [ ] This should be implemented as an extension
     * [ ] Could be triggered with a key binding (and/or override open file)
     * [ ] Need to refactor App class to support views instead of just files
     * [ ] A view could be an editor or an extension ui
     * [ ] Extensions should be able to control both status bars and key legend


## Rationale
For many the command line is a different environment for text editing.
Most coders are familiar with GUI text editors and for many vi and emacs
have a too steep learning curve. For them (like for me) nano was the weapon of
choice. But nano feels clunky and it has its limitations. That's why
I wrote my own editor with built in multi cursor support to fix the situation.
Another reason is that developing Suplemon is simply fun to do.
