# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Eval(Module):
    def run(self, app, editor, args):
        if not args:
            app.set_status("Please enter an expression to evaluate.")
            return False
        try:
            value = eval(args)
        except:
            app.set_status("Eval failed.")
            return False
        app.set_status("Result:{0}".format(value))
        return True

module = {
    "class": Eval,
    "name": "eval",
}
