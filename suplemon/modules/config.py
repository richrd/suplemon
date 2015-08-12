# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Config(Module):
    """Shortcut to openning the current config file."""

    def run(self, app, editor, args):
        path = app.config.path()
        f = app.file_is_open(path)
        if f:
            app.switch_to_file(app.get_file_index(f))
        else:
            if not app.open_file(path):
                app.new_file(path)
            app.switch_to_file(app.last_file_index())

module = {
    "class": Config,
    "name": "config",
}
