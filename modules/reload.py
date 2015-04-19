from mod_base import *

class Reload(Command):
    def init(self):
        #self.bind_key("^R")
        pass
        
    def run(self, app, editor):
        self.app.init_keys()
        self.app.modules.load()

module = {
    "class": Reload,
    "name": "reload",
}
