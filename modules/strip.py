from mod_base import *


class Strip(Command):
    def init(self):
        self.bind_key("^B")  # Used to bind a key to the run method

    def run(self, app, editor):
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.data = line.data.strip()

module = {
    "class": Strip,
    "name": "strip",
}
