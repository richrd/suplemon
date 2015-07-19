# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""

__version__ = "0.1.22"

import os
import sys

import ui
import modules
import themes
import helpers

from logger import *
from config import *
from editor import *
from file import *


class App:
    def __init__(self, filenames=None):
        """
        Handle App initialization

        :param list filenames: Names of files to load initially
        :param str filenames[*]: Path to a file to load
        """
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
        self.event_bindings = {}

        # Define core operations
        self.operations = {
            "help": self.help,
            "save_file": self.save_file,
            "run_command": self.run_command,
            "find": self.find,
            "go_to": self.go_to,
            "open": self.open,
            "close_file": self.close_file,
            "new_file": self.new_file,
            "ask_exit": self.ask_exit,
            "prev_file": self.prev_file,
            "next_file": self.next_file,
            "save_file_as": self.save_file_as,
            "reload_file": self.reload_file,
            "toggle_mouse": self.toggle_mouse,
            "toggle_fullscreen": self.toggle_fullscreen,
        }

        # Load core components
        self.logger = Logger()
        self.config = Config(self)
        self.config.load()
        self.ui = ui.UI(self)  # Load user interface
        self.ui.init()

        # Load extension modules
        self.modules = modules.ModuleLoader(self)
        self.modules.load()

        # Load themes
        self.themes = themes.ThemeLoader(self)

        # Save filenames for later
        self.filenames = filenames

        # Indicate that windows etc. have been created.
        self.inited = 1

    def log(self, text, log_type=LOG_ERROR):
        """Add text to the log buffer."""
        self.logger.log(text, log_type)

    def init(self):
        """Run the app via the ui wrapper."""
        self.ui.run(self.run)

    def exit(self):
        """Stop the main loop and exit."""
        self.running = 0

    def run(self, *args):
        """Run the app."""
        # Load ui and files etc
        self.load()
        # Initial render
        self.get_editor().resize()
        self.ui.refresh()
        # Start mainloop
        self.main_loop()
        # Unload ui
        self.ui.unload()

    def load(self):
        """Load the app."""
        self.ui.load()
        ver = sys.version_info
        if ver[0] < 3 or (ver[0] == 3 and ver[1] < 3):
            ver = ".".join(map(str, sys.version_info[0:2]))
            msg = "Running Suplemon with Python "+ver
            msg += " which isn't officialy supported. "
            msg += "Please use Python 3.3 or higher."
            self.log(msg, LOG_WARNING)
        self.load_files()
        self.running = 1
        self.trigger_event_after("app_loaded")

    def main_loop(self):
        """Run the terminal IO loop until exit() is called."""
        while self.running:
            # Update ui before refreshing it
            self.ui.update()
            # See if we have input to process
            event = self.ui.get_input()
            if event:
                # self.log("INPUT:"+str(event), LOG_INFO)
                # Handle the input or give it to the editor
                if not self.handle_input(event):
                    # Pass the input to the editor component
                    self.get_editor().handle_input(event)
                # TODO: why do I need resize here?
                # (View won't update after switching files, WTF)
                self.trigger_event_after("mainloop")
                self.get_editor().resize()
                self.ui.refresh()

    def get_status(self):
        """Set the status message."""
        return self.status_msg

    def get_file_index(self, file_obj):
        """Get file index by file object."""
        return self.files.index(file_obj)

    def get_key_bindings(self):
        """Returns the list of key bindings."""
        return self.config["app"]["keys"]

    def get_event_bindings(self):
        """Returns the dict of event bindings."""
        return self.event_bindings

    def set_key_binding(self, key, operation):
        """Bind a key to an operation."""
        self.get_key_bindings()[key] = operation

    def set_event_binding(self, event, when, callback):
        """Bind a callbacks to be run before or after an event."""
        event_bindings = self.get_event_bindings()
        if when not in event_bindings.keys():
            event_bindings[when] = {}
        if event in event_bindings[when].keys():
            event_bindings[when][event].append(callback)
        else:
            event_bindings[when][event] = [callback]

    def set_status(self, s):
        """Set the status message."""
        self.status_msg = str(s)

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
        key_bindings = self.get_key_bindings()
        if event.key_name in key_bindings.keys():
            operation = key_bindings[event.key_name]
        elif event.key_code in key_bindings.keys():
            operation = key_bindings[event.key_code]
        else:
            return False
        self.run_operation(operation)
        return True

    def handle_mouse(self, event):
        """Handle a mouse event."""
        editor = self.get_editor()
        if event.mouse_code == 1:                    # Left mouse button release
            editor.set_single_cursor(event.mouse_pos)
        elif event.mouse_code == 4096:               # Right mouse button release
            editor.add_cursor(event.mouse_pos)
        elif event.mouse_code == 524288:             # Wheel up
            editor.page_up()
        elif event.mouse_code == 134217728:          # Wheel down(and unfortunately left button drag)
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
        if len(self.files) < 2:
            return
        cur = self.current_file
        cur += 1
        if cur > len(self.files)-1:
            cur = 0
        self.switch_to_file(cur)

    def prev_file(self):
        """Switch to previous file."""
        if len(self.files) < 2:
            return
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
        if input_str is False:
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
        self.logger.log("Looking for command '" + cmd + "'", LOG_INFO)
        if cmd in self.modules.modules.keys():
            self.logger.log("Trying to run command '" + cmd + "'", LOG_INFO)
            self.get_editor().store_action_state(cmd)
            self.modules.modules[cmd].run(self, self.get_editor())
        else:
            self.set_status("Command '" + cmd + "' not found.")
        return True

    def run_operation(self, operation):
        """Run an app core operation."""
        # Support arbitrary callables
        if hasattr(operation, '__call__'):
            operation()
        elif operation in self.operations.keys():
            # cancel = self.trigger_event(operation)
            cancel = self.trigger_event_before(operation)
            if not cancel:
                result = self.operations[operation]()
            # Run post action event
            # self.trigger_event("after:" + operation)
            self.trigger_event_after(operation)
            return result
        return False

    def trigger_event(self, event, when):
        """Triggers event and runs registered callbacks."""
        status = False
        bindings = self.get_event_bindings()
        if not when in bindings.keys():
            return False
        if event in bindings[when].keys():
            callbacks = bindings[when][event]
            for cb in callbacks:
                try:
                    val = cb(event)
                except:
                    self.log(get_error_info())
                    continue
                if val:
                    status = True
        return status

    def trigger_event_before(self, event):
        return self.trigger_event(event, "before")

    def trigger_event_after(self, event):
        return self.trigger_event(event, "after")

    def toggle_fullscreen(self):
        """Toggle full screen editor."""
        display = self.config["display"]
        if display["show_top_bar"]:
            display["show_top_bar"] = 0
            display["show_bottom_bar"] = 0
            display["show_legend"] = 0
        else:
            display["show_top_bar"] = 1
            display["show_bottom_bar"] = 1
            display["show_legend"] = 1
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
        if self.get_file().is_changed():
            if not self.ui.query_bool("Close file?"):
                return False
        self.files.pop(self.current_file)
        if not len(self.files):
            self.new_file()
            return False
        if self.current_file == len(self.files):
            self.current_file -= 1

    def save_file(self, file=False):
        """Save current file."""
        f = file or self.get_file()
        if not f.get_name():
            return self.save_file_as(f)
        if f.save():
            self.set_status("Saved [" + helpers.curr_time_sec() + "] '" + f.name + "'")
            if f.path() == self.config.path():
                self.reload_config()
            return True
        self.set_status("Couldn't write to '" + f.name + "'")
        return False

    def save_file_as(self, file=False):
        """Save current file."""
        f = file or self.get_file()
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
        if self.filenames:
            for name in self.filenames:
                if os.path.isdir(name):
                    continue
                if self.file_is_open(name):
                    continue
                if not self.open_file(name):
                    self.new_file(name)
        # If nothing was loaded
        if not self.files:
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
