suplemon
========
          ___________   _________  ___     ______________________________   ___ 
         /  _____/  /  /  /  _   \/  /\   /  ______/        /  ___   /   | /  /\
        /  /____/  /  /  /  /_/  /  / /  /  /_____/  /  /  /  /  /  /    |/  / /
       /____   /  /  /  /  _____/  / /  /  ______/  /  /  /  /  /  /  /|    / /
      _____/  /  /__/  /  /\___/  /____/  /_____/  /  /  /  /__/  /  / |   / /
     /_______/\_______/__/ /  /_______/________/__/__/__/________/__/ /|__/ /
     \_______\ \______\__\/   \_______\________\__\__\__\________\__\/ \__\/

Command line text editor with multicursor support. The goal is to replicate sublimetext style functionality in the terminal.

# Suplemon multicursor editing:
![Suplemon in action](http://bittemple.org/misc/suplemon/suplemon-demo.gif)

# Goals:
 1. [X] Create a command line text editor with built in multi cursor support. Damn it's amazing!
 2. [X] Usability should be as good and easy as nano.
 3. [X] Multi cursor ~~and multi selection~~ should be comparable to sublimetext.
 4. [X] Develop suplemon with suplemon!!!
 5. [ ] World domination!

# Usage:

    python3 main.py [filename]...

Must use python3 for proper character encoding support.

# Features
 * Terminal text editing with style
 * Proper multi cursor editing, Sublime Text style. Blessed!
 * Copy & Paste, with multi line support
 * Find and Find next
 * Multiple files
 * Comming later:
     * Selections
     * Extensions

# Keyboard shortcuts:

 * Alt + Arrow Keys
   > Add new curors in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word

 * ESC
   > Revert to a single cursor

 * Ctrl + W
   > Duplicate line
  
 * Ctrl + X
   > Cut line(s) to buffer

 * Ctrl + V
   > Insert buffer

 * Ctrl + G
   > Go to line number or file

 * Ctrl + F
   > Find text

 * Ctrl + D
   > Find next (add a new cursor at the next occurance)

 * Alt + Page Up
   > Move line(s) up

 * Alt + Page Down
   > Move line(s) down

 * F1
   > Save current file

 * F2
   > Reload current file
   
 * F5
   > Undo
   
 * F6
   > Redo

 * F9
   > Toggle line numbers

 * Ctrl + O
   > Open file

 * Ctrl + Page Up
   > Switch to next file

 * Ctrl + Page Down
   > Switch to previous file


# Todo
 * [ ] New file and close file
 * [ ] Read only viewer
 * [ ] Custom key bindings
 * [ ] Setting for enabling undo for cursor changes
 * [ ] File selector, kind of like what nano has
 * [ ] EITHER Close files one at a time with 'save?' prompt.
 * [ ] OR     Store files and cursor positions for restoring later
 * [ ] Auto complete
 * [ ] Selections
 * [ ] Proper syntax higlighting
 * [ ] Editor plugins/extensions/macros
 * [ ] ...
 * [X] Undo / Redo
 * [X] Move config file to user home directory
 * [X] File type detection for highlighting
 * [X] Duplicate line (without clipboard)
 * [X] Use semver 
 * [X] Nano-like menu and keyboard shortcuts with legend. TODO: respect future custom bindings
 * [X] Go to file as well as line number 
 * [X] Show if file is edited
 * [X] Copy / Paste buffer
 * [X] Proper status bar information
 * [X] Jump to end of whitespace with home key 
 * [X] Command line for getting input
 * [X] Line number toggling
 * [X] Loading multiple files and switching between them
 * [X] Live config reloading when it's modified
 * [X] Line based syntax highlighting

# Fix / Defects
 * [ ] Cursors sometimes left hanging at non existent coordinates (eg. when file reloaded)
 * [ ] Fill in incomplete config file with defaults
 * [ ] With multpile lines selected pressing backspace and enter makes changes (shouldn't)
 * [ ] Add 'remove previous cursor' function
 * [ ] Delete key when cursor at line end; add dedicated setting.
 * [ ] Encoding errors
 * [ ] Finish refactoring viewer.py and editor.py
 * [X] Can't open files like '~/.suplemon-config.json'
 * [X] Cursor invisible when at end of scrolled line
 * [X] Esc key effect is delayed
 * [X] Fixed: Find starts at top of file instead of current ~~cursor~~ line
 * [X] Start find at current line AND column
 * [X] Make editor white color brighter (not gray)
 * [X] Show editor at top of terminal when show_top_bar == False 
