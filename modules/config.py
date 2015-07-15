from mod_base import *


class Config(Command):
    def run(self, app, editor):
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
