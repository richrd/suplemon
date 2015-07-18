# -*- encoding: utf-8
"""
Config handler.
"""

import os
import json
import curses  # Get key definitons

from helpers import *


class Config:
    def __init__(self, app):
        self.app = app
        self.filename = ".suplemon-config.json"
        self.fpath = os.path.expanduser("~")
        self.defaults = {
            "app": {
                # Print debug logging
                "debug": 1,
                # How long curses will wait to detect ESC key
                "escdelay": 50,
                # Wether to use special unicode symbols for decoration
                "use_unicode_symbols": 0,
                # Key bindings for app functions
                "keys": {
                    "^H": "help",               # Ctrl + H
                    "^S": "save_file",          # Ctrl + S
                    "^E": "run_command",        # Ctrl + E
                    "^F": "find",               # Ctrl + F
                    "^G": "go_to",              # Ctrl + G
                    "^O": "open",               # Ctrl + O
                    "^K": "close_file",         # Ctrl + K
                    "^N": "new_file",           # Ctrl + N
                    "^X": "ask_exit",           # Ctrl + X
                    554: "next_file",           # Ctrl + Page Up
                    549: "prev_file",           # Ctrl + Page Down
                    "kNXT5": "next_file",       # Ctrl + Page Up
                    "kPRV5": "prev_file",       # Ctrl + Page Down
                    265: "save_file_as",        # F1
                    266: "reload_file",         # F2
                    272: "toggle_mouse",        # F8
                    275: "toggle_fullscreen",   # F12
                }
            },
            "editor": {
                # Indent new lines to same level as previous line
                "auto_indent_newline": True,
                # Character to use for end of line
                "end_of_line": "\n",
                # Unindent with backspace
                "backspace_unindent": True,
                # Cursor style. 'reverse' or 'underline'
                "cursor": "reverse",
                "default_encoding": "utf-8",
                # Number of spaces to insert when pressing tab
                "tab_width": 4,
                # Amount of undo states to store
                "max_history": 50,
                # Characters considered to separate words
                "punctuation": " (){}[]<>$@!%'\"=+-/*.:,;_\n\r",
                # Character to use to visualize end of line
                "line_end_char": "",
                # White space characters and their visual matches
                "white_space_map": {
                    " ": "\u00B7",       # Show space as interpunct
                    "\t": "\u21B9",      # Tab as tab symbol
                    "\u00A0": "\u00B7",  # Show nonbreaking space as interpunct
                    "\u00AD": "\u2423",  # Soft hyphen as letter shelf
                    "\u200B": "\u00B7"   # Zero width space as interpunct
                },
                # Wether to visually show white space chars
                "show_white_space": False,
                "show_line_nums": True,
                "show_line_colors": True,
                "show_highlighting": True,
                "theme": "monokai",
                "use_mouse": False,
                # Wether to use copy/paste across multiple files
                "use_global_buffer": True,
                # Find with regex by default
                "regex_find": False,
                # Key bindings for editor functions
                "keys": {
                    curses.KEY_UP: "arrow_up",            # Up
                    curses.KEY_DOWN: "arrow_down",        # Down
                    curses.KEY_LEFT: "arrow_left",        # Left
                    curses.KEY_RIGHT: "arrow_right",      # Right
                    curses.KEY_ENTER: "enter",            # Enter
                    "\n": "enter",                        # Enter
                    "^J": "enter",                        # Enter (for 'getch')
                    curses.KEY_BACKSPACE: "backspace",    # Backspace
                    "^?": "backspace",                    # Backspace (Mac fix)
                    curses.KEY_DC: "delete",              # Delete
                    331: "insert",                        # Insert
                    "\t": "tab",                          # Tab
                    "^I": "tab",                          # Tab
                    353: "untab",                         # Shift + Tab
                    curses.KEY_HOME: "home",              # Home
                    curses.KEY_END: "end",                # End
                    "^[": "escape",                       # Escape
                    563: "new_cursor_up",                 # Alt + Up
                    522: "new_cursor_down",               # Alt + Down
                    542: "new_cursor_left",               # Alt + Left
                    557: "new_cursor_right",              # Alt + Right
                    "kUP3": "new_cursor_up",              # Alt + Up
                    "kDN3": "new_cursor_down",            # Alt + Down
                    "kLFT3": "new_cursor_left",           # Alt + Left
                    "kRIT3": "new_cursor_right",          # Alt + Right
                    curses.KEY_PPAGE: "page_up",          # Page Up
                    curses.KEY_NPAGE: "page_down",        # Page Down
                    552: "push_up",                       # Alt + Page Up
                    547: "push_down",                     # Alt + Page Down
                    "kPRV3": "push_up",                   # Alt + Page Up
                    "kNXT3": "push_down",                 # Alt + Page Down
                    269: "undo",                          # F5
                    270: "redo",                          # F6
                    273: "toggle_line_nums",              # F9
                    274: "toggle_line_ends",              # F10
                    275: "toggle_highlight",              # F11
                    "^C": "cut",                          # Ctrl + C
                    "^W": "duplicate_line",               # Ctrl + W
                    "^V": "insert",                       # Ctrl + V
                    "^D": "find_next",                    # Ctrl + D
                    "^A": "find_all",                     # Ctrl + A
                    544: "jump_left",                     # Ctrl + Left
                    559: "jump_right",                    # Ctrl + Right
                    565: "jump_up",                       # Ctrl + Up
                    524: "jump_down",                     # Ctrl + Down
                    "kLFT5": "jump_left",                 # Ctrl + Left
                    "kRIT5": "jump_right",                # Ctrl + Right
                    "kUP5": "jump_up",                    # Ctrl + Up
                    "kDN5": "jump_down",                  # Ctrl + Down
                }
            },
            "display": {
                "show_top_bar": True,
                "show_app_name": True,
                "show_file_list": True,
                "show_legend": True,
                "show_bottom_bar": True,
                "invert_status_bars": True,
            },
        }

        self.config = dict(self.defaults)

    def log(self, s):
        self.app.log(s)

    def path(self):
        return os.path.join(self.fpath, self.filename)

    def load(self):
        path = self.path()
        if os.path.exists(path):
            try:
                f = open(path)
                data = f.read()
                f.close()
                self.config = json.loads(data)
                self.merge_defaults(self.config)
                return True
            except:
                self.log("Failed to load config file!")
                self.log(get_error_info())
        return False

    def reload(self):
        """Reload the config file."""
        return self.load()

    def store(self):
        """Write current config state to file."""
        data = json.dumps(self.config)
        f = open(self.filename)
        f.write(data)
        f.close()

    def merge_defaults(self, config):
        """Fill any missing config options with defaults."""
        for prim_key in self.defaults.keys():
            curr_item = self.defaults[prim_key]
            if prim_key not in config.keys():
                config[prim_key] = dict(curr_item)
                continue
            for sec_key in curr_item.keys():
                if sec_key not in config[prim_key].keys():
                    config[prim_key][sec_key] = curr_item[sec_key]
        self.merge_keys(config)
        return config

    def merge_keys(self, config):
        """Fill in config with default keys."""
        # Do merge for app and editor keys
        for dest in ["app", "editor"]:
            key_config = config[dest]["keys"]
            key_defaults = self.defaults[dest]["keys"]
            for key in key_defaults.keys():
                # Fill in each key that's not defined yet
                if key not in key_config.keys():
                    key_config[key] = key_defaults[key]

    def __getitem__(self, i):
        """Get a config variable."""
        return self.config[i]

    def __setitem__(self, i, v):
        """Set a config variable."""
        self.config[i] = v

    def __str__(self):
        """Convert entire config array to string."""
        return str(self.config)

    def __len__(self):
        """Return length of top level config variables."""
        return len(self.config)
