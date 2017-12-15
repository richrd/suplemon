# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Reload(Module):
    """Reload all add-on modules."""

    def run(self, app, editor, args):
        self.app.modules.load()


module = {
    "class": Reload,
    "name": "reload",
}
