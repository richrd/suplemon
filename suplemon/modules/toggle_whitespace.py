# -*- encoding: utf-8

from suplemon_module import Module


class ToggleWhitespace(Module):
    def init(self):
        # Bind a key to the run-method
        self.bind_key(271)  # F7

    def run(self, app, editor, args):
        # Toggle the boolean
        new_value = not self.app.config["editor"]["show_white_space"]
        self.app.config["editor"]["show_white_space"] = new_value

module = {
    "class": ToggleWhitespace,
    "name": "toggle_whitespace",
}
