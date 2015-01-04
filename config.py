#-*- encoding: utf-8
import os
import json
from helpers import *

class Config:
    def __init__(self, parent):
        self.parent = parent
        self.filename = ".suplemon-config.json"
        self.fpath = os.path.expanduser("~")
        self.defaults = {
            "app": {
                "remember_open_files": False,
                "debug": False,
            },
            "editor": {
                "auto_indent_newline": True,
                "cursor": "reverse", # reverse or underline
                "default_encoding": "utf-8",
                "max_history": 20,
                "tab_width": 4,
                "punctuation": " (){}[]'\"=+-/*.:,;_", # for jumping between words
                "line_end_char": "",
                "show_line_nums": True,
                "show_line_colors": True,
                "show_highlighting": False,
            },
            "display": {
                "show_top_bar": True,
                "show_app_name": True,
                "show_clock": True,
                "show_file_list": True,
                "show_legend": True,
                "show_bottom_bar": True,
                "show_last_key": False,
                "show_term_size": False
            },
        }

        self.config = dict(self.defaults)

    def log(self, s):
        self.parent.status(s)

    def err(self, s):
        self.parent.logger.log(s)

    def path(self):
        return os.path.join(self.fpath, self.filename)

    def load(self):
        # TODO: fill in missing/invalid config with defaults
        try:
            path = self.path()
            f = open(path)
            data = f.read()
            f.close()
            self.config = json.loads(data)
            self.merge_defaults(self.config)
            return True
        except:
            self.err(get_error_info())
            self.log("Failed to load config file!")
        return False

    def reload(self):
        return self.load()
        
    def store(self):
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
        return self.config[i]

    def __setitem__(self, i, v):
        self.config[i] = v

    def __str__(self):
        return str(self.config)

    def __len__(self):
        return len(self.config)
