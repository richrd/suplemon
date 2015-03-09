from mod_base import *

class Config(Command):
    def __init__(self):
        pass

    def run(self, app, editor):
        if not app.open_file("~/.suplemon-config.json"):
            app.new_file("~/.suplemon-config.json")
        app.switch_to_file(app.last_file())
 
module = {
    "class": Config,
    "name": "config",
}
