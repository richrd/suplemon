# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class Paste(Module):
    """Toggle paste mode (helpful when pasting over SSH if auto indent is enabled)"""

    def init(self):
        # Flag for paste mode
        self.active = False
        # Initial state of auto indent
        self.auto_indent_active = self.app.config["editor"]["auto_indent_newline"]
        # Listen for config changes
        self.bind_event_after("config_loaded", self.config_loaded)

    def run(self, app, editor, args):
        # Simply toggle pastemode when the command is run
        self.active = not self.active
        self.set_paste_mode(self.active)
        self.show_confirmation()
        return True

    def config_loaded(self, e):
        # Refresh the auto indent state when config is reloaded
        self.auto_indent_active = self.app.config["editor"]["auto_indent_newline"]

    def get_status(self):
        # Return the paste mode status for the statusbar
        return "[PASTEMODE]" if self.active else ""

    def show_confirmation(self):
        # Show a status message when pastemode is toggled
        state = "activated" if self.active else "deactivated"
        self.app.set_status("Paste mode " + state)

    def set_paste_mode(self, active):
        # Enable or disable auto indent
        if active:
            self.app.config["editor"]["auto_indent_newline"] = False
        else:
            self.app.config["editor"]["auto_indent_newline"] = self.auto_indent_active


module = {
    "class": Paste,
    "name": "paste",
    "status": "bottom",
}
