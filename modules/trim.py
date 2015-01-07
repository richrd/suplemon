from mod_base import *

class Trim(Command):
    def __init__(self):
        pass

    def run(self, app, editor):
        for line in editor.lines:
            line.data = line.data.rstrip()

module = {
    "class": Trim,
    "name": "trim",
}