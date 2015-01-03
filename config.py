#-*- encoding: utf-8
import os
import json
from helpers import *

class Config:
    def __init__(self, parent):
        self.parent = parent
        self.filename = ".suplemon-config.json"
        self.fpath = os.path.expanduser("~")
        #self.fpath = os.path.dirname(os.path.realpath(__file__))
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
            },
            "display": {
                "show_top_bar": True,
                "show_app_name": True,
                "show_clock": True,
                "show_file_list": True,
                "show_legend": False,
                "show_bottom_bar": True,
                "show_line_nums": True,
                "show_line_colors": True,
                "line_end_char": "",
                "show_highlighting": False,
                "show_last_key": True,
                "show_term_size": True
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
 
    def __getitem__(self, i):
        return self.config[i]

    def __setitem__(self, i, v):
        self.config[i] = v

    def __str__(self):
        return str(self.config)

    def __len__(self):
        return len(self.config)
