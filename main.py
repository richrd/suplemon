#!/usr/bin/python3
#-*- encoding: utf-8
"""
The main class that starts and runs Suplemon.
"""

__version__ = "0.1.0"

import os
import sys
import time
import curses

import ui
import modules

from helpers import *
from logger import *
from config import *
from editor import *
from file import *

class App:
    def __init__(self):
        self.version = __version__
        self.inited = 0
        self.running = 0

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.files = []
        self.current_file = 0
        self.status_msg = ""
        self.last_input = None

        # Load core components
        self.logger = Logger()
        self.config = Config(self)
        self.config.load()
        self.ui = ui.UI(self) # Load user interface

        # Load extension modules
        self.modules = modules.ModuleLoader(self)
        self.modules.load()

        # Indicate that windows etc. have been created.
        self.inited = 1

    def log(self, text, log_type=LOG_ERROR):
        """Add text to the log buffer."""
        self.logger.log(text, log_type)

    def load(self):
        """Load the app."""
        self.ui.load()
        self.load_files()
        loaded = True

    def exit(self):
        """Stop the main loop and exit."""
        self.running = 0

    def run(self):
        """Run the app."""
        # Load ui and files etc
        self.load()
        self.running = 1
        # Initial render
        self.get_editor().resize()
        self.ui.refresh()
        # Start mainloop
        self.main_loop()
        # Unload ui
        self.ui.unload()

    def main_loop(self):
        """Run the terminal IO loop until exit() is called."""
        while self.running:
            # Update ui before refreshing it
            self.ui.update()
            # See if we have input to process
            value = self.ui.get_input()
            if value:
                # Handle the input or give it to the editor
                if not self.handle_input(value):
                    # Pass the input to the editor component
                    self.get_editor().got_input(value)
                #TODO: why do I need resize here? (View won't update after switching files, WTF)
                self.get_editor().resize()
                self.ui.refresh()

    def set_status(self, s):
        """Set the status message."""
        self.status_msg = str(s)

    def get_status(self):
        """Set the status message."""
        return self.status_msg

    def get_file_index(self, file_obj):
        """Get file index by file object."""
        return self.files.index(file_obj)

    def unsaved_changes(self):
        """Check if there are unsaved changes in any file."""
        for f in self.files:
            if f.is_changed():
                return True
        return False

    def reload_config(self):
        """Reload configuration."""
        self.config.reload()
        for f in self.files:
            self.setup_editor(f.editor)        
        self.resize()
        self.refresh()

    def handle_input(self, value):
        """Handle a key input event."""
        self.last_input = value
        key, name = value

        if name == "^H": self.help()                 # Ctrl + H
        elif name == "^E": self.run_command()        # Ctrl + E
        elif name == "^F": self.find()               # Ctrl + F
        elif name == "^G": self.go_to()              # Ctrl + G
        elif name == "^O": self.open()               # Ctrl + O
        elif name == "^K": self.close_file()         # Ctrl + K
        elif name == "^N": self.new_file()           # Ctrl + N
        elif name == "^X": self.ask_exit()           # Ctrl + X

        elif key == 554: self.prev_file()            # Ctrl + Page Up
        elif key == 549: self.next_file()            # Ctrl + Page Down
        elif key == 265: self.save_file()            # F1
        elif key == 266: self.reload_file()          # F2
        elif key == 272: self.toggle_mouse()         # F8
        elif key == 275: self.toggle_fullscreen()    # F12

        elif key == curses.KEY_MOUSE:                # Mouse events
            mouse_state = self.ui.get_mouse_state()
            if mouse_state:
                self.handle_mouse(mouse_state)
        else:
            return False
        return True

    def handle_mouse(self, state):
        """Handle a mouse event."""
        #TODO: implement this
        self.last_input = state
        pass

    ###########################################################################
    # User Interactions
    ###########################################################################

    def help(self):
        """Open help file."""
        f = self.default_file()
        f.set_data("Sorry, no help here yet!")
        self.files.append(f)
        self.switch_to_file(self.last_file_index())

    def new_file(self):
        """Open new empty file."""
        self.files.append(self.default_file())
        self.current_file = self.last_file_index()

    def ask_exit(self):
        """Exit if no unsaved changes, else make sure the user really wants to exit."""
        if self.unsaved_changes():
            yes = self.ui.query_bool("Exit?")
            if yes:
                self.exit()
                return True
            return False
        else:
            self.exit()
            return True

    def switch_to_file(self, index):
        """Load a default file if no files specified."""
        self.current_file = index

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

    def go_to(self):
        """Go to a line or a file."""
        result = self.ui.query("Go to:")
        try:
            result = int(result)
            self.get_editor().go_to_pos(result)
        except:
            index = self.find_file(result)
            if index != -1:
                self.switch_to_file(index)
        return True

    def find(self):
        """Find in file."""
        what = self.ui.query("Find:")
        if what:
            self.get_editor().find(what)

    def find_file(self, s):
        """Return index of file matching string."""
        i = 0
        for file in self.files:
            if file.name[:len(s)].lower() == s.lower():
                return i
            i += 1
        return -1

    def run_command(self):
        """Run editor commands."""
        data = self.ui.query("Command:")
        if not data:
            return False
        if data == "fail": #log debug
            try: # to
                fail
            except:
                self.log(get_error_info())
        parts = data.split(" ")
        cmd = parts[0].lower()
        self.logger.log("Looking for command '" + cmd +"'", LOG_INFO)
        if cmd in self.modules.modules.keys():
            self.logger.log("Trying to run command '" + cmd +"'", LOG_INFO)
            self.get_editor().store_action_state(cmd)
            self.modules.modules[cmd].run(self, self.get_editor())
        return True

    def toggle_fullscreen(self):
        """Toggle full screen editor."""
        display = self.config["display"]
        if display["show_top_bar"]:
            display["show_top_bar"] = 0
            display["show_bottom_bar"] = 0
        else:
            display["show_top_bar"] = 1
            display["show_bottom_bar"] = 1
        # Virtual curses windows need to be resized
        self.ui.resize()

    def toggle_mouse(self):
        """Toggle mouse support."""
        # Invert the boolean
        self.config["editor"]["use_mouse"] = not self.config["editor"]["use_mouse"]
        self.ui.setup_mouse()

    ###########################################################################
    # Editor operations
    ###########################################################################

    def new_editor(self):
        """Create a new editor instance."""
        editor = Editor(self, self.ui.editor_win)
        self.setup_editor(editor)
        return editor

    def get_editor(self):
        """Return the current editor."""
        return self.files[self.current_file].editor

    def setup_editor(self, editor):
        """Setup an editor instance with configuration."""
        config = self.config["editor"]
        editor.set_config(config)

    ###########################################################################
    # File operations
    ###########################################################################

    def open(self):
        """Ask for file name and try to open it."""
        name = self.ui.query("Open file:")
        if not name:
            return False
        exists = self.file_is_open(name)
        if exists:
            self.switch_to_file(self.files.index(exists))
            return True

        if not self.open_file(name):
            self.set_status("Failed to load '" + name + "'")
            return False
        self.switch_to_file(self.last_file_index())
        return True

    def close_file(self):
        """Close current file if user confirms action."""
        if self.ui.query_bool("Close file?"):
            self.files.pop(self.current_file)
            if not len(self.files):
                self.new_file()
                return False
            if self.current_file == len(self.files):
                self.current_file -= 1

    def save_file(self):
        """Save current file."""
        f = self.get_file()
        name = self.ui.query("Save as:", f.name)
        if not name:
            return False
        f.set_name(name)
        if f.save():
            self.set_status("Saved [" + curr_time_sec() + "] '" + f.name + "'")
            if f.path() == self.config.path():
                self.reload_config()
            return True
        self.set_status("Couldn't write to '" + f.name + "'")
        return False

    def reload_file(self):
        """Reload the current file."""
        if self.ui.query_bool("Reload '" + self.get_file().name + "'?"):
            if self.get_file().reload():
                return True
        return False
        
    def get_files(self):
        """Return list of open files."""
        return self.files

    def get_file(self):
        """Return the current file."""
        return self.files[self.current_file]


    def last_file_index(self):
        """Get index of last file."""
        cur = len(self.files)-1
        return cur

    def current_file_index(self):
        """Get index of current file."""
        return self.current_file

    def open_file(self, filename):
        """Open a file."""
        file = File(self)
        file.set_path(filename)
        file.set_editor(self.new_editor())
        if not file.load():
            return False
        self.files.append(file)
        return True

    def load_files(self):
        """Try to load all files specified in arguments."""
        #TODO: use argparse (this won't work for quoted filenames)
        if len(sys.argv) > 1:
            names = sys.argv[1:]
            for name in names:
                if self.file_is_open(name): continue
                if self.open_file(name):
                    loaded = True
                else:
                    self.new_file(name)
        else:
            self.load_default()

    def file_is_open(self, path):
        """Check if file is open. Returns the File object or False."""
        for file in self.files:
            if file.path() == os.path.abspath(path):
                return file
        return False

    def load_default(self):
        """Load a default file if no files specified."""
        file = self.default_file()
        self.files.append(file)

    def default_file(self):
        """Create the default file."""
        file = File(self)
        file.set_editor(self.new_editor())
        # Set markdown as the default file type
        file.editor.set_file_extension("md")
        return file


def main(*args):
    global app
    app = App()
    app.run()

if __name__ == "__main__":
    """Only run the app if it's run directly (not imported)."""
    curses.wrapper(main)

    # Output log info
    if app.config["app"]["debug"]:
        app.logger.output()
