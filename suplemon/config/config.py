# -*- encoding: utf-8

import os
import logging

import json5

# TODO: Language specific configuration


def merge_defaults(defaults, config):
    """Recursivley merge two dicts."""
    for key in defaults.keys():
        item = defaults[key]
        if key not in config.keys():
            config[key] = item
            continue
        if not isinstance(item, dict):
            continue
        config[key] = merge_defaults(item, config[key])
    return config


def load_config_file(file_path):
    """Load a JSON5 config file."""
    with open(file_path, "r") as f:
        data = f.read()
    config = json5.loads(data)
    return config


class ConfigLoader(object):
    """Generic config loader."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "defaults")
        self.config_filename = "config.json"
        self.keymap_filename = "keymap.json"

        self.default_config = None
        self.default_keymap = None

        self.config_path = os.path.join(os.path.expanduser("~"), ".config", "suplemon")

    def init(self):
        self.create_config_path()
        return self.load_defaults()

    def load_defaults(self):
        self.default_config = self.load_file(os.path.join(self.default_path, self.config_filename))
        self.default_keymap = self.load_file(os.path.join(self.default_path, self.keymap_filename))

        # Return whether both configs were successfully loaded (can't run without them)
        return self.default_config is not None and self.default_keymap is not None

    def load_user_config(self):
        config = Config(self.default_config, os.path.join(self.config_path, self.config_filename))
        config.load()
        return config

    def load_user_keymap(self):
        config = Config(self.default_keymap, os.path.join(self.config_path, self.keymap_filename))
        config.load()
        return config

    def load_file(self, path):
        try:
            return load_config_file(path)
        except FileNotFoundError:
            self.logger.error("Config file not found at '{}'".format(path))
        except ValueError:
            self.logger.exception("Config at '{}' is malformed!".format(path))

    def create_config_path(self):
        if not os.path.exists(self.config_path):
            try:
                os.makedirs(self.config_path)
            except:
                self.logger.warning(
                    "Config folder '{}' doesn't exist and couldn't be created.".format(self.config_path)
                )


class Config(object):
    """A container for configs."""
    def __init__(self, defaults, path):
        self.logger = logging.getLogger(__name__)
        self.defaults = defaults
        self.path = path
        self.config = None

    def load(self):
        self.config = self.defaults  # Fallback
        try:
            config = load_config_file(self.path)
        except FileNotFoundError:
            self.logger.debug("User config file not found at '{}'".format(self.path))
            return
        except ValueError:
            self.logger.exception("Config at '{}' is malformed!".format(self.path))
            return
        self.config = merge_defaults(self.defaults, config)

    def __getitem__(self, i):
        """Get a config variable."""
        return self.config[i]

    def __setitem__(self, i, v):
        """Set a config variable."""
        self.config[i] = v
