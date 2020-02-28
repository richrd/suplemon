# -*- encoding: utf-8

import subprocess

from suplemon.suplemon_module import Module

import pyperclip

class SystemClipboard(Module):
    """Integrates the system clipboard with suplemon."""

    def init(self):
        self.init_logging(__name__)
        self.bind_event_before("insert", self.insert)
        self.bind_event_after("copy", self.copy)
        self.bind_event_after("cut", self.copy)

    def copy(self, event):
        lines = self.app.get_editor().get_buffer()
        data = "\n".join([str(line) for line in lines])
        self.set_clipboard(data)

    def insert(self, event):
        data = self.get_clipboard()
        lines = data.split("\n")
        self.app.get_editor().set_buffer(lines)

    def get_clipboard(self):
        return pyperclip.paste()

    def set_clipboard(self, data):
        pyperclip.copy(data)


module = {
    "class": SystemClipboard,
    "name": "system_clipboard",
}
