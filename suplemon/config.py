# -*- encoding: utf-8
"""
Config handler.
"""

import os
import json
import logging

from . import helpers


class Config:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.default_filename = "defaults.json"
        self.config_filename = "suplemon-config.json"
        self.home_dir = os.path.expanduser("~")
        self.fpath = os.path.join(self.home_dir, ".config", "suplemon")

        self.defaults = {}
        self.config = {}

    def init(self):
        self.create_config_dir()
        return self.load_defaults()

    def path(self):
        return os.path.join(self.fpath, self.config_filename)

    def set_path(self, path):
        parts = os.path.split(path)
        self.fpath = parts[0]
        self.config_filename = parts[1]

    def load(self):
        path = self.path()
        config = False
        if not os.path.exists(path):
            self.logger.debug("Configuration file '{0}' doesn't exist.".format(path))
        else:
            config = self.load_config_file(path)
        if config:
            self.logger.debug("Loaded configuration file '{0}'".format(path))
            self.config = self.merge_defaults(config)
        else:
            self.logger.info("Failed to load config file '{0}'.".format(path))
            self.config = dict(self.defaults)
            return False
        return config

    def load_defaults(self):
        path = os.path.join(self.app.path, "config", self.default_filename)
        if not os.path.exists(path):
            return False
        defaults = self.load_config_file(path)
        if not defaults:
            self.logger.warning("Failed to load default config file! ('{0}')".format(path))
            return False
        self.defaults = defaults
        return True

    def reload(self):
        """Reload the config file."""
        return self.load()

    def store(self):
        """Write current config state to file."""
        data = json.dumps(self.config)
        f = open(self.config_filename)
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

    def load_config_file(self, path):
        try:
            f = open(path)
            data = f.read()
            f.close()
            data = self.remove_config_comments(data)
            config = json.loads(data)
            return config
        except:
            return False

    def remove_config_comments(self, data):
        """Remove comments from a 'pseudo' JSON config file.

        Removes all lines that begin with '#' or '//' ignoring whitespace.

        :param data: Commented JSON data to clean.
        :return: Cleaned pure JSON.
        """
        lines = data.split("\n")
        cleaned = []
        for line in lines:
            line = line.strip()
            if helpers.starts(line, "//") or helpers.starts(line, "#"):
                continue
            cleaned.append(line)
        return "\n".join(cleaned)

    def create_config_dir(self):
        if not os.path.exists(self.fpath):
            try:
                os.makedirs(self.fpath)
            except:
                self.app.logger.warning("Config folder '{0}' doesn't exist and couldn't be created.".format(
                                        self.fpath))

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
