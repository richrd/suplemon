suplemon
========
          ___________   _________  ___     ______________________________   ___
         /  _____/  /  /  /  _   \/  /\   /  ______/        /  ___   /   | /  /\
        /  /____/  /  /  /  /_/  /  / /  /  /_____/  /  /  /  /  /  /    |/  / /
       /____   /  /  /  /  _____/  / /  /  ______/  /  /  /  /  /  /  /|    / /
      _____/  /  /__/  /  /\___/  /____/  /_____/  /  /  /  /__/  /  / |   / /
     /_______/\_______/__/ /  /_______/________/__/__/__/________/__/ /|__/ /
     \_______\ \______\__\/   \_______\________\__\__\__\________\__\/ \__\/

Command line text editor with multicursor support. The goal is to replicate sublimetext style functionality in the terminal with the ease of use of Nano.

# Suplemon multicursor editing:
![Suplemon in action](http://bittemple.org/misc/suplemon/suplemon-demo.gif)

# Usage:

    python3 main.py [filename]...

*Must use python3 for proper character encoding support.*
*Tested on Unix.*

# Features
 * Terminal text editing with style
 * Proper multi cursor editing, Sublime Text style. Blessed!
 * Easy Undo/Redo
 * Multiple files in tabs
 * Powerful Go To feature for jumping to files and lines
 * Copy & Paste, with multi line support
 * Find and Find next
 * Extensions (easy to write your own)
 * Might be comming later:
     * Selections

# Goals:
 1. [X] Create a command line text editor with built in multi cursor support. Damn it's amazing!
 2. [X] Usability should be as good and easy as nano.
 3. [X] Multi cursor ~~and multi selection~~ should be comparable to Sublimetext.
 4. [X] Develop Suplemon with Suplemon!!! I already use Suplemon for all command line editing,
        Git commits, and a lot of developement.

# Keyboard shortcuts:

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

 * Ctrl + F
   > Find string

 * Ctrl + D
   > Find next (add a new cursor at the next occurance)

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

 * F1
   > Save current file

 * F2
   > Reload current file

 * F5
   > Undo

 * F6
   > Redo

 * F8
   > Toggle mouse mode

 * F9
   > Toggle line numbers

 * F11
   > Toggle full screen

 * Ctrl + O
   > Open file

 * Ctrl + Page Up
   > Switch to next file

 * Ctrl + Page Down
   > Switch to previous file


# Todo
 * [ ] Custom key bindings
 * [ ] Combine line based highlighters and other language related data (include comment syntax etc)
 * [ ] CSS highlighter
    * ~~And disable editing~~ Don't disable editing to enable save as.
 * [ ] Comment line command (TODO: add lang detection)
 * [ ] EXT: Feature to automatically add ; to end of lines
    * [ ] Generalized: add prepend and append commands
 * [ ] Regex find/search (make configurable instead of a new feature?)
 * [ ] Global clipboard (copy from one file to another)
 * [ ] Read only viewer
 * [ ] Setting for enabling/disabling undo for cursor changes
 * [ ] File selector, kind of like what nano has
 * [ ] EITHER Close files one at a time with 'save?' prompt.
 * [ ] OR     Store files and cursor positions for restoring later
 * [ ] Auto complete
 * [ ] Selections
 * [ ] Proper syntax higlighting
 * [ ] Indicate if file isn't writable (in status bar). Use os.access(path, os.W_OK)
 * [X] Prompt for close or exit confirmation only when file(s) have been modified
 * [X] Indicate if file was saved successfully or if it failed
 * [X] Better yes/no query for exit (and in general)
 * [X] Generic linelighter for generic highlighting
 * [X] Editor plugins/extensions/macros
   * [ ] Design proper API
   * [X] Trim command to get rid of trailing whitespace
   * [X] Lower/Upper/Reverse lettercase (todo: reverse case)
   * [X] Reverse line
 * [X] New file and close file
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

# Ideas?
 * Refactor higher level commands/functions into modular plugins.
 * ...

# Fix / Defects
 * [ ] Can't open files that have spaces in them.
 * [ ] Remember find query if occurance not found (jump to top of file)
 * [ ] Syntax specific commenting.
 * [ ] Display tab characters with a replacement char (tab messes up lines)
 * [ ] Slightly unreliable undo/redo.
 * [ ] Cut command fails with multiple cursors when one is on last line
 * [ ] Finish refactoring viewer.py and editor.py
   * [ ] Optimize rendering for ssh (minimal screen update)
   * [ ] Only refresh cursors when moving around
   * [ ] Only refresh modified lines when editing
 * [ ] With multpile lines selected pressing backspace and enter makes changes (shouldn't) 
 * [ ] Refine find and find_next commands.
   * [X] Fix 'finding' empty character. Revert to 'add_cursor_right'.
   * [X] Better auto find with ctrl+d. (Find the current word or character)
   * [X] Forget last find on esc.
   * [ ] Don't forget find text automatically when using Ctrl + F 
 * [X] Return code 0 on exit:
       Curses forces code 130 and causes git to ignore saved commit message, argh!
 * [X] Config extension double loads config file, instead of switching to it
 * [X] Encoding errors 
 * [X] Remove "Failed to load config." when file doesn't exist
 * [X] Delete key when cursor at line end; ~~add dedicated setting~~ made to work as normal.
 * [X] Make adding cursors up and down smarter: add them at main cursor x coordinate if possible
 * [X] Saving file into a directory stores the relative path as the filename.
 * [X] Cursors sometimes left hanging at non existent coordinates (eg. when file reloaded)
       Solved by rectifying all cursors in move_cursors. Should optimize more in callers.
 * [X] Remove debug logging in non-debug mode
 * [X] Fill in incomplete config file with defaults
 * [X] Add 'remove previous cursor' function (fixed with undo/redo)
 * [X] Can't open files like '~/.suplemon-config.json'
 * [X] Cursor invisible when at end of scrolled line
 * [X] Esc key effect is delayed
 * [X] Fixed: Find starts at top of file instead of current ~~line~~ cursor
 * [X] Start find at current line AND column
 * [X] Make editor white color brighter (not gray)
 * [X] Show editor at top of terminal when show_top_bar == False
