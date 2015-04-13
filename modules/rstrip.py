from mod_base import *

class RStrip(Command):
    def run(self, app, editor):
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.data = line.data.rstrip()

module = {
    "class": RStrip,
    "name": "rstrip",
}