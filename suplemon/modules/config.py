# -*- encoding: utf-8

import os

from suplemon import config


class SuplemonConfig(config.ConfigModule):
    """Shortcut to openning the keymap config file."""
    def init(self):
        self.conf_name = "defaults.json"
        self.conf_default_path = os.path.join(self.app.path, "config", self.conf_name)
        self.conf_user_path = self.app.config.path()

module = {
    "class": SuplemonConfig,
    "name": "config",
}
