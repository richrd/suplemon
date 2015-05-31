from mod_base import *

class Reload(Command):
    def run(self, app, editor):
        self.app.modules.load()

module = {
    "class": Reload,
    "name": "reload",
}
