# -*- encoding: utf-8

import os

from suplemon import config


class KeymapConfig(config.ConfigModule):
    """Shortcut to openning the keymap config file."""
    def __init__(self, app):
        config.ConfigModule.__init__(self, app)

    def init(self):
        self.conf_name = "keymap.json"
        self.conf_default_path = os.path.join(self.app.path, "config", self.conf_name)
        self.conf_user_path = self.app.config.keymap_path()

module = {
    "class": KeymapConfig,
    "name": "keymap",
}
