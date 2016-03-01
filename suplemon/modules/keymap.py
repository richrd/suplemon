# -*- encoding: utf-8

import os

from suplemon.suplemon_module import Module


class Keymap(Module):
    """Shortcut to openning the current config file."""

    def run(self, app, editor, args):
        if args == "defaults":
            # Open the default config in a new file only for viewing
            path = os.path.join(app.path, "config", "keymap.json")
            self.open_read_only(app, path)
        else:
            # Open the user config file for editing
            path = app.config.keymap_path()
            f = app.file_is_open(path)
            if f:
                app.switch_to_file(app.get_file_index(f))
            else:
                if not app.open_file(path):
                    app.new_file(path)
                app.switch_to_file(app.last_file_index())

    def open_read_only(self, app, path):
        f = open(path)
        data = f.read()
        f.close()
        file = app.new_file()
        file.set_name("keymap.json")
        file.set_data(data)
        app.switch_to_file(app.last_file_index())

module = {
    "class": Keymap,
    "name": "keymap",
}
