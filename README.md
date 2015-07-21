suplemon :lemon: [![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=master)](https://travis-ci.org/richrd/suplemon)
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

## Installation
Try it out! Installation is as easy as pulling the repo.

    git clone https://github.com/richrd/suplemon.git

**The master branch is considered stable.**

No dependencies outside the Python Standard Library required.

Dev Branch Status: [![Build Status](https://travis-ci.org/richrd/suplemon.svg?branch=dev)](https://travis-ci.org/richrd/suplemon)

### Optional dependencies

 * Pygments
 > For support for syntax highlighting over 300 languages.
 
 * Flake8
 > For showing linting for Python files.
 

## Usage

    python3 cli.py [filename]...

**Must use Python 3.3 for proper character encoding support.**

*Lower Python versions might work, but aren't officially supported.*

*Tested on Unix.*

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
 * Multiple files in tabs
 * Powerful Go To feature for jumping to files and lines
 * Find and Find next
 * Copy & Paste, with multi line support
 * Custom keyboard shortcuts
 * Mouse support
 * Extensions (easy to write your own)
 * Lots more...

## Goals
 1. [X] Create a command line text editor with built in multi cursor support. It's awesome!
 2. [X] Usability should be as good and easy as nano.
 3. [X] Multi cursor should be comparable to Sublime Text.
 4. [X] Develop Suplemon with Suplemon!!! I've used Suplemon for a long time as my main
        editor (replacing ST and nano) for all developement, Git commits etc.

## Configuration

The suplemon config file is stored at ```~/.config/suplemon/suplemon-config.json```.

The best way to edit it is to run the ```config``` command (Run commands via ```Ctrl+E```).
That way Suplemon will automatically reload the configuration when you save the file.
You can find all the configuration options and descriptions in the suplemon/config.py file.


## Keyboard shortcuts

 * Ctrl + X
   > Exit

 * Ctrl + C
   > Cut line(s) to buffer

 * Ctrl + V
   > Insert buffer

 * Ctrl + W
   > Duplicate line

 * Ctrl + G
   > Go to line number or file (type the beginning of a filename to switch to it). 
   > You can also use 'filena:42' to go to line 42 in filename.py etc.

 * Ctrl + F
   > Search for a string or regular expression (configurable)

 * Ctrl + D
   > Search for next occurance or find the word the cursor is on. Adds a new cursor at each new occurance.

 * Alt + Arrow Key
   > Add new curor in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word

 * ESC
   > Revert to a single cursor

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
have a too steep learing curve. For them (like for me) nano was the weapon of
choice. But nano feels clunky and it has its limitations. That's why
I wrote my own editor with built in multi cursor support to fix the situation.
Another reason is that developing Suplemon is simply fun to do.
