# -*- coding:utf-8
from mod_base import *


class ReplaceAll(Command):
    def run(self, app, editor):
        r_from = self.app.ui.query("Replace text:")
        if not r_from:
            return False
        r_to = self.app.ui.query("Replace with:")
        if not r_to:
            return False
        for file in app.get_files():
            file.editor.replace_all(r_from, r_to)

module = {
    "class": ReplaceAll,
    "name": "replace_all",
}
