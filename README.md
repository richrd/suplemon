suplemon
========

Command line text editor with multicursor support. The goal is to replicate sublimetext style functionality in the terminal.

#Goals:
 1. [X] Create a command line text editor with built in multi cursor support. Damn it's amazing!
 2. [/] Usability should be as good and easy as nano.
 3. [X] Multi cursor and multi selection should be comparable to sublimetext.
 4. [X] Develop suplemon with suplemon!!!

#Usage:

    python main.py [filename]

#Keyboard shortcuts:

 * Alt + Arrow Keys
   > Add new curors in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word
 
 * ESC
   > Revert to a single cursor
   
 * Ctrl + X
   > Delete line(s)

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
   > Toggle line numbers.
   
   
# To-Do
 * [ ] Nano-like menu and keyboard shortcuts with legend
 * [X] Proper status bar information
 * [X] Jump to end of whitespace with home key 
 * [X] Command line for getting input
 * [X] Line number toggling
 * [ ] Loading multiple files and switching between them
 * [ ] Config and storing open cursor positions for restoring later
 * [ ] Syntax higlighting
 * [ ] Editor plugins
 * ...
 
# Fix
 * [ ] Delete key when cursor at line end
 
 