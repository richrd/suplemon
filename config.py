#-*- encoding: utf-8
"""
Config handler.
"""

import os
import json

from helpers import *

class Config:
    def __init__(self, app):
        self.app = app
        self.filename = ".suplemon-config.json"
        self.fpath = os.path.expanduser("~")
        self.defaults = {
            "app": {
                # Print debug logging
                "debug": False,
                # How long curses will wait to detect ESC key
                "escdelay": 50,
                # Wether to use special unicode symbols for decoration
                "use_unicode_symbols": 0,
            },
            "editor": {
                # Indent new lines to same level as previous line
                "auto_indent_newline": True,
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
                "punctuation": " (){}[]'\"=+-/*.:,;_",
                # Character to use to visualize end of line
                "line_end_char": "",
                # White space characters and their visual matches
                "white_space_map": {
                    " ": "\u00B7",        # Show space as interpunct
                    "\t": "\u21B9",       # Tab as tab symbol
                    "\u00AD": "\u2423",   # Soft hyphen as letter shelf
                    "\u200B": "\u00B7"    # Zero width space as interpunct
                },
                #"white_space": " ",
                # Wether to visually show white space chars
                "show_white_space": False,
                "show_line_nums": True,
                "show_line_colors": True,
                "show_highlighting": False,
                "use_mouse": False,
                # Wether to use copy/paste across multiple files
                "use_global_buffer": True,
                # Find with regex by default
                "regex_find": False,
            },
            "display": {
                "show_top_bar": True,
                "show_app_name": True,
                "show_file_list": True,
                "show_legend": True,
                "show_bottom_bar": True
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
                if not sec_key in config[prim_key].keys():
                    config[prim_key][sec_key] = curr_item[sec_key]
        return config
 
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
