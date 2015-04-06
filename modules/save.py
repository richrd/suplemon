from mod_base import *

class Save(Command):
    def __init__(self):
        pass

    def run(self, app, editor):
        return app.save_file()

module = {
    "class": Save,
    "name": "save",
}
