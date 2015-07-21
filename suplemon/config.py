# -*- encoding: utf-8
"""
Config handler.
"""

import os
import json
import logging


class Config:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.filename = "suplemon-config.json"
        self.home_dir = os.path.expanduser("~")
        self.fpath = os.path.join(self.home_dir, ".config", "suplemon")

        self.defaults = {
            # Global settings
            "app": {
                # Print debug logging
                "debug": 1,
                # How long curses will wait to detect ESC key
                "escdelay": 50,
                # Wether to use special unicode symbols for decoration
                "use_unicode_symbols": 0,
                # Key bindings for app functions
                "keys": {
                    "ctrl+h": "help",              # Ctrl + H
                    "ctrl+s": "save_file",         # Ctrl + S
                    "ctrl+e": "run_command",       # Ctrl + E
                    "ctrl+f": "find",              # Ctrl + F
                    "ctrl+g": "go_to",             # Ctrl + G
                    "ctrl+o": "open",              # Ctrl + O
                    "ctrl+w": "close_file",        # Ctrl + W
                    "ctrl+n": "new_file",          # Ctrl + N
                    "ctrl+x": "ask_exit",          # Ctrl + X
                    "ctrl+p": "comment",           # Ctrl + P
                    "ctrl+pageup": "next_file",    # Ctrl + Page Up
                    "ctrl+pagedown": "prev_file",  # Ctrl + Page Down
                    "f1": "save_file_as",          # F1
                    "f2": "reload_file",           # F2
                    "f8": "toggle_mouse",          # F8
                    "f11": "toggle_fullscreen",    # F11
                }
            },
            # Editor settings
            "editor": {
                # Indent new lines to same level as previous line
                "auto_indent_newline": True,
                # Character to use for end of line
                "end_of_line": "\n",
                # Unindent with backspace
                "backspace_unindent": True,
                # Cursor style. 'reverse' or 'underline'
                "cursor_style": "reverse",
                # Encoding for reading and writing files
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
                # Line numbering
                "show_line_nums": True,
                # Naive line highlighting
                "show_line_colors": True,
                # Proper syntax highlighting
                "show_highlighting": True,
                # Syntax highlighting theme
                "theme": "monokai",
                # Listen for mouse events
                "use_mouse": False,
                # Wether to use copy/paste across multiple files
                "use_global_buffer": True,
                # Find with regex by default
                "regex_find": False,
                # Key bindings for editor functions
                "keys": {
                    "up": "arrow_up",                 # Up
                    "down": "arrow_down",             # Down
                    "left": "arrow_left",             # Left
                    "right": "arrow_right",           # Right
                    "enter": "enter",                 # Enter
                    "backspace": "backspace",         # Backspace
                    "delete": "delete",               # Delete
                    "insert": "insert",               # Insert
                    "tab": "tab",                     # Tab
                    "shift+tab": "untab",             # Shift + Tab
                    "home": "home",                   # Home
                    "end": "end",                     # End
                    "escape": "escape",               # Escape
                    "pageup": "page_up",              # Page Up
                    "pagedown": "page_down",          # Page Down
                    "f5": "undo",                     # F5
                    "f6": "redo",                     # F6
                    "f9": "toggle_line_nums",         # F9
                    "f10": "toggle_line_ends",        # F10
                    "f11": "toggle_highlight",        # F11
                    "alt+up": "new_cursor_up",        # Alt + Up
                    "alt+down": "new_cursor_down",    # Alt + Down
                    "alt+left": "new_cursor_left",    # Alt + Left
                    "alt+right": "new_cursor_right",  # Alt + Right
                    "alt+pageup": "push_up",          # Alt + Page Up
                    "alt+pagedown": "push_down",      # Alt + Page Down
                    "ctrl+c": "cut",                  # Ctrl + C
                    "ctrl+k": "duplicate_line",       # Ctrl + K
                    "ctrl+v": "insert",               # Ctrl + V
                    "ctrl+d": "find_next",            # Ctrl + D
                    "ctrl+a": "find_all",             # Ctrl + A
                    "ctrl+left": "jump_left",         # Ctrl + Left
                    "ctrl+right": "jump_right",       # Ctrl + Right
                    "ctrl+up": "jump_up",             # Ctrl + Up
                    "ctrl+down": "jump_down",         # Ctrl + Down
                }
            },
            # UI Display Settings
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
                self.logger.info("Loaded configuration file '{}'".format(path))
                return True
            except:
                self.logger.warning("Failed to load config file!", exc_info=True)
                return False
        self.logger.info("Configuration file '{}' doesn't exist.".format(path))
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
