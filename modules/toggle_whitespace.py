from mod_base import *

class ToggleWhitespace(Command):
    def init(self):
        self.bind_key(271) # Used to bind a key to the run-method
        
    def run(self, app, editor):
        self.app.config["editor"]["show_white_space"] = not self.app.config["editor"]["show_white_space"]

module = {
    "class": ToggleWhitespace,
    "name": "toggle_whitespace",
}