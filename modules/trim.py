from mod_base import *

class Trim(Command):
    def run(self, app, editor):
        lines = editor.get_lines_with_cursors()
        for line in lines:
            line.data = line.data.rstrip()

module = {
    "class": Trim,
    "name": "trim",
}