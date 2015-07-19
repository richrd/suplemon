# -*- encoding: utf-8

from suplemon_module import Module


class Eval(Module):
    def run(self, app, editor, args):
        value = eval(args)
        app.set_status("Eval:{}".format(value))

module = {
    "class": Eval,
    "name": "eval",
}
