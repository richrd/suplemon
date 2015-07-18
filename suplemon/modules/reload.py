# -*- encoding: utf-8

from suplemon_module import Module


class Reload(Module):
    def run(self, app, editor, args):
        self.app.modules.load()

module = {
    "class": Reload,
    "name": "reload",
}
