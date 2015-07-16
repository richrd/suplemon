from mod_base import *


class ToggleWhitespace(Command):
    def init(self):
        # Bind a key to the run-method
        self.bind_key(271)  # F7

    def run(self, app, editor):
        # Toggle the boolean
        new_value = not self.app.config["editor"]["show_white_space"]
        self.app.config["editor"]["show_white_space"] = new_value

module = {
    "class": ToggleWhitespace,
    "name": "toggle_whitespace",
}
