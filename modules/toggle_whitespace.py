from mod_base import *

class ToggleWhitespace(Command):
    def init(self):
        # Bind a key to the run-method
        self.bind_key(271) # F7
        
    def run(self, app, editor):
        # Toggle the boolean
        self.app.config["editor"]["show_white_space"] = not self.app.config["editor"]["show_white_space"]

module = {
    "class": ToggleWhitespace,
    "name": "toggle_whitespace",
}