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

# Goals:
 1. [X] Create a command line text editor with built in multi cursor support. Damn it's amazing!
 2. [ ] Usability should be as good and easy as nano. TODO: add keyboard legend.
 3. [X] Multi cursor and multi selection should be comparable to sublimetext.
 4. [X] Develop suplemon with suplemon!!!
 5. [ ] World domination!

# Usage:

    python main.py [filename]

# Suplemon multicursor editing:
![Suplemon in action](http://bittemple.org/misc/suplemon/digits1.gif)

# Features
 * Terminal text editing with style
 * Proper multi cursor editing, Sublime Text style. Blessed!
 * Copy & Paste, with multi line support
 * Find and Find next
 * Comming later:
     * Multiple files
     * Selections
     * Extensions

# Keyboard shortcuts:

 * Alt + Arrow Keys
   > Add new curors in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word
 
 * ESC
   > Revert to a single cursor
   
 * Ctrl + X
   > Cut line(s) to buffer
   
 * Insert
   > Insert buffer

 * Ctrl + G
   > Go to line number
   
 * Ctrl + F
   > Find text
   
 * Ctrl + D
   > Add a new cursor at the next occurance
 
 * Alt + Page Up
   > Move line(s) up
 
 * Alt + Page Down
   > Move line(s) down
   
 * F1
   > Save current file
   
 * F2
   > Reload current file
   
 * F9
   > Toggle line numbers
   
   
# To-Do
 * [ ] Nano-like menu and keyboard shortcuts with legend
 * [X] Copy / Paste buffer
 * [X] Proper status bar information
 * [X] Jump to end of whitespace with home key 
 * [X] Command line for getting input
 * [X] Line number toggling
 * [ ] Loading multiple files and switching between them
 * [ ] Config and storing open cursor positions for restoring later
 * [ ] Syntax higlighting
 * [ ] Editor plugins
 * ...
 
# Fix / Defects
 * [X] Fixed: Find starts at top of file instead of current cursor
 * [ ] Delete key when cursor at line end
 * [ ] Add 'remove previous cursor' function
 * [ ] Make editor white color brighter (not gray)
 * [ ] With multpile lines selected pressing backspace and enter makes changes (shouldn't)