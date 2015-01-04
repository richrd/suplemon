#!/usr/bin/python
#-*- coding:utf-8
"""
The main class that starts and runs Suplemon.
"""

__version__ = "0.0.1"

import os
import sys
import time

import ui
from logger import *
from config import *
from editor import *
from helpers import *

from file import *

quick_help = """
Welcome to suplemon!
====================

Usage: ```python main.py [filename]...```


Warning: beta software, bugs may occur.

# Keyboard shortcuts:

 * Alt + Arrow Keys
   > Add new curors in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word
 
 * ESC
   > Revert to a single cursor
   
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
   
 * F9
   > Toggle line numbers
 
 * Ctrl + O
   > Open file
   
 * Ctrl + Page Up
   > Switch to next file
 
 * Ctrl + Page Down
   > Switch to previous file

"""


class App(ui.UI):
    def __init__(self):
        self.version = __version__
        self.inited = 0
        self.running = 0
        self.last_key = None
        self.status_msg = ""
        self.capturing = 0

        self.files = []
        self.current_file = 0

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.logger = Logger()
        self.config = Config(self)
        self.config.load()
        ui.UI.__init__(self) # Load user interface
        self.inited = 1 # Indicate that windows etc. have been created.

    def toggle_fullscreen(self):
        """Toggle full screen editor."""
        display = self.config["display"]
        if display["show_top_bar"]:
            display["show_top_bar"] = 0
            display["show_bottom_bar"] = 0
        else:
            display["show_top_bar"] = 1
            display["show_bottom_bar"] = 1
        self.resize()
        self.refresh()

    def log(self, text):
        """Add text to log."""
        self.logger.log(text)
        self.status(text)

    # TODO: Non curses methods start here (to later separate ui from functionality)
    def setup_editor(self, editor):
        """Setup an editor instance with configuration."""
        config = self.config["editor"]
        editor.set_config(config)

    def reload_config(self):
        """Reload configuration."""
        self.config.reload()
        for f in self.files:
            self.setup_editor(f.editor)        
        self.resize()
        self.refresh()

    def resize_editor(self):
        """Resize the editor window."""
        yx = self.screen.getmaxyx()
        xy = self.size()
        height = self.max_editor_height()
        self.editor().resize( (height, yx[1]) )

    def refresh(self):
        """Refresh the UI."""
        self.editor().render()
        self.refresh_status()
        self.screen.refresh()

    def update(self):
        self.refresh()

    def status(self, s):
        """Set the status message."""
        self.status_msg = str(s)
        self.refresh_status()

    def file(self):
        """Return the current file."""
        return self.files[self.current_file]

    def editor(self):
        """Return the current editor."""
        return self.files[self.current_file].editor

    def file_exists(self, path):
        """Check if file is open."""
        for file in self.files:
            if file.path() == os.path.abspath(path):
                return file
        return False

    def go_to(self):
        """Go to a line or a file."""
        result = self.query("Go to:")
        try:
            result = int(result)
            self.editor().go_to_pos(result)
        except:
            index = self.find_file(result)
            if index != -1:
                self.switch_to_file(index)
        return True

    def find(self):
        """Find in file."""
        what = self.query("Find:")
        if what:
            self.editor().find(what)

    def find_file(self, s):
        """Find index of file matching string."""
        i = 0
        for file in self.files:
            if file.name[:len(s)].lower() == s.lower():
                return i
            i += 1
        return -1
        
    def new_editor(self):
        """Create a new editor instance."""
        editor = Editor(self, self.editor_win)
        self.setup_editor(editor)
        return editor

    def open(self):
        """Ask for file name and try to open it."""
        name = self.query("Open:")
        if not name:
            return False
        exists = self.file_exists(name)
        if exists:
            self.switch_to_file(self.files.index(exists))
            return True

        if not self.open_file(name):
            self.status("Failed to load '"+name+"'")
            return False
        self.switch_to_file(self.last_file())
        return True

    def save(self):
        """Save current file app."""
        fi = self.file()
        name = self.query("Save as:", fi.name)
        if not name:
            return False
        fi.set_name(name)
        if fi.save():
            self.status("Saved [" + curr_time_sec() + "] '" + fi.name + "'")
            if fi.path() == self.config.path():
                self.reload_config()
            return True
        self.status("Couldn't write to '" + fi.name + "'")
        return False

    def open_file(self, filename, new = False):
        """Open a file."""
        result = ""
        file = File(self)
        file.set_path(filename)
        file.set_editor(self.new_editor())
        loaded = file.load()
        if not loaded and not new:
            return False
        self.files.append(file)
        return loaded

    def load_default(self):
        """Load a default file if no files specified."""
        file = self.default_file()
        file.set_data(quick_help)
        self.files.append(file)

    def default_file(self):
        """Create the default file."""
        file = File(self)
        file.set_editor(self.new_editor())
        file.editor.set_file_extension("md")
        return file

    def reload(self):
        """Reload the current file."""
        if self.query("Reload '"+self.file().name+"'?"):
            if self.file().reload():
                return True
        return False

    def switch_to_file(self, index):
        """Load a default file if no files specified."""
        self.current_file = index
        self.resize_editor()
        self.refresh()

    def next_file(self):
        """Switch to next file."""
        if len(self.files) < 2: return
        cur = self.current_file
        cur += 1
        if cur > len(self.files)-1:
            cur = 0
        self.switch_to_file(cur)

    def prev_file(self):
        """Switch to previous file."""
        if len(self.files) < 2: return
        cur = self.current_file
        cur -= 1
        if cur < 0:
            cur = len(self.files)-1
        self.switch_to_file(cur)

    def last_file(self):
        """Get index of last file."""
        cur = len(self.files)-1
        return cur
        
    def help(self):
        """Open help file."""
        f = self.default_file()
        f.set_data(quick_help)
        self.files.append(f)
        self.switch_to_file(self.last_file())

    def run_command(self):
        """Run editor commands."""
        # TODO: Replace this with command modules
        data = self.query("Eval:")
        res = ""
        try:
            res = eval(data)
        except:
            res = "[ERROR]"
        self.status(res)
        return True
    
    def handle_char(self, char):
        """Handle a character from curses."""
        editor = self.editor()
        if char == 265: self.save()                 # F1
        elif char == 266: self.reload()             # F2
        elif char == 276: self.toggle_fullscreen()  # F12
        elif char == 8: self.help()                 # Ctrl + H
        elif char == 5: self.run_command()          # Ctrl + E
        elif char == 6: self.find()                 # Ctrl + F
        elif char == 7: self.go_to()                # Ctrl + G
        elif char == 15: self.open()                # Ctrl + O
        elif char == 410: pass                      # Mouse events?
        elif char == 554: self.prev_file()          # Ctrl + Page Up
        elif char == 549: self.next_file()          # Ctrl + Page Down
        else:
            return False
        return True
        
    def keyboard_interrupt(self):
        """Handle a keyboard interrupt."""
        try:
            yes = self.query("Exit?")
        except:
            self.running = 0
            return True
        if yes:
            self.running = 0
            return True
        return False

    def load(self):
        """Load the app."""
        loaded = True
        if len(sys.argv) > 1:
            names = sys.argv[1:]
            for name in names:
                if self.file_exists(name): continue
                if self.open_file(name):
                    loaded = True
                else:
                    self.open_file(name, new=True)
        else:
            self.load_default()

    def run(self):
        """Run the app."""
        self.load()
        self.running = 1
        self.refresh()
        while self.running:
            editor = self.editor()
            self.check_resize()
            try:
                char = self.screen.getch()
                self.last_key = char
            except KeyboardInterrupt:
                if self.keyboard_interrupt():
                    break
                continue
                
            if not self.handle_char(char):
                editor.got_chr(char)
            self.refresh_status()
            self.refresh()

        curses.endwin()

def main(*args):
    global app
    app = App()
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)

# Output log info
app.logger.output()
