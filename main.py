#!/usr/bin/python3
#-*- encoding: utf-8
"""
The main class that starts and runs Suplemon.
"""

__version__ = "0.1.7"

import os
import sys
import time

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

        # Set default variables
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.files = []
        self.current_file = 0
        self.status_msg = ""
        self.last_input = None
        self.global_buffer = []
        self.init_keys()

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

    def init_keys(self):
        self.key_bindings = {
            "^H": self.help,               # Ctrl + H
            "^S": self.save_file,          # Ctrl + S
            "^E": self.run_command,        # Ctrl + E
            "^F": self.find,               # Ctrl + F
            "^G": self.go_to,              # Ctrl + G
            "^O": self.open,               # Ctrl + O
            "^K": self.close_file,         # Ctrl + K
            "^N": self.new_file,           # Ctrl + N
            "^X": self.ask_exit,           # Ctrl + X
            554: self.prev_file,           # Ctrl + Page Up
            549: self.next_file,           # Ctrl + Page Down
            265: self.save_file_as,        # F1
            266: self.reload_file,         # F2
            272: self.toggle_mouse,        # F8
            275: self.toggle_fullscreen,   # F12
        }

    def set_key_binding(self, key, callback):
        self.key_bindings[key] = callback

    def log(self, text, log_type=LOG_ERROR):
        """Add text to the log buffer."""
        self.logger.log(text, log_type)

    def load(self):
        """Load the app."""
        if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 3):
            ver = ".".join(map(str, sys.version_info[0:2]))
            self.log("Running Suplemon with Python "+ver+" which isn't officialy supported. Please use Python 3.3 or higher.", LOG_WARNING)
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
            event = self.ui.get_input()
            if event:
                #self.log("INPUT:"+str(event), LOG_INFO)
                # Handle the input or give it to the editor
                if not self.handle_input(event):
                    # Pass the input to the editor component
                    self.get_editor().handle_input(event)
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
        self.ui.resize()
        self.ui.refresh()

    def handle_input(self, event):
        """Handle an input event."""
        if not event:
            return False
        self.last_input = event

        if event.type == "key":
            return self.handle_key(event)
        elif event.type == "mouse":
            return self.handle_mouse(event)
        return False

    def handle_key(self, event):
        """Handle a keyboard event."""
        if event.key_name in self.key_bindings.keys():
            self.key_bindings[event.key_name]()
        elif event.key_code in self.key_bindings.keys():
            self.key_bindings[event.key_code]()
        else:
            return False
        return True

    def handle_mouse(self, event):
        """Handle a mouse event."""
        editor = self.get_editor()
        if event.mouse_code == 1:                    # Left mouse button release
            editor.set_single_cursor(event.mouse_pos)
        elif event.mouse_code == 134217728:          # Wheel up (and unfortunately left button drag)
            editor.page_up()
        elif event.mouse_code == 524288:             # Wheel down
            editor.page_down()
        else:
            return False
        return True

    ###########################################################################
    # User Interactions
    ###########################################################################

    def help(self):
        """Open help file."""
        f = self.default_file()
        import help
        f.set_data(help.help_text)
        self.files.append(f)
        self.switch_to_file(self.last_file_index())

    def new_file(self, path=None):
        """Open new empty file."""
        new_file = self.default_file()
        if path:
            new_file.set_path(path)
        self.files.append(new_file)
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
        """Go to a line or a file (or a line in a specific file with 'name:lineno')."""
        input_str = self.ui.query("Go to:")
        lineno = None
        fname = None
        if input_str == False:
            return False
        if input_str.find(":") != -1:
            parts = input_str.split(":")
            fname = parts[0]
            lineno = parts[1]
            file_index = self.find_file(fname)
            if file_index != -1:
                self.switch_to_file(file_index)
                try:
                    input_str = int(lineno)
                    self.get_editor().go_to_pos(input_str)
                except:
                    pass
        else:
            try:
                line_no = int(input_str)
                self.get_editor().go_to_pos(line_no)
            except:
                file_index = self.find_file(input_str)
                if file_index != -1:
                    self.switch_to_file(file_index)

    def find(self):
        """Find in file."""
        editor = self.get_editor()
        what = self.ui.query("Find:", editor.last_find)
        if what:
            editor.find(what)

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
        parts = data.split(" ")
        cmd = parts[0].lower()
        self.logger.log("Looking for command '" + cmd +"'", LOG_INFO)
        if cmd in self.modules.modules.keys():
            self.logger.log("Trying to run command '" + cmd +"'", LOG_INFO)
            self.get_editor().store_action_state(cmd)
            self.modules.modules[cmd].run(self, self.get_editor())
        else:
            self.set_status("Command '" + cmd + "' not found.")
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
        if self.config["editor"]["use_mouse"]:
            self.set_status("Mouse enabled")
        else:
            self.set_status("Mouse disabled")

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
        flag = True
        if self.get_file().is_changed():
            if not self.ui.query_bool("Close file?"):
                flag = False
        self.files.pop(self.current_file)
        if not len(self.files):
            self.new_file()
            return False
        if self.current_file == len(self.files):
            self.current_file -= 1

    def save_file(self, file = False):
        """Save current file."""
        f = file or self.get_file()
        if f.save():
            self.set_status("Saved [" + curr_time_sec() + "] '" + f.name + "'")
            if f.path() == self.config.path():
                self.reload_config()
            return True
        self.set_status("Couldn't write to '" + f.name + "'")
        return False

    def save_file_as(self):
        """Save current file."""
        f = self.get_file()
        name = self.ui.query("Save as:", f.name)
        if not name:
            return False
        f.set_name(name)
        return self.save_file(f)

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
        #TODO: Maybe use argparse for this
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
        # Specify contents to avoid appearing as modified
        file.set_data("")
        # Set markdown as the default file type
        file.editor.set_file_extension("md")
        return file


def main(*args):
    global app
    app = App()
    app.run()

if __name__ == "__main__":
    """Only run the app if it's run directly (not imported)."""
    ui.wrapper(main)
    # Output log info
    if app.config["app"]["debug"]:
        app.logger.output()
