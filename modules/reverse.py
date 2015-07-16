from mod_base import *


class Reverse(Command):
    def run(self, app, editor):
        line_nums = []
        for cursor in editor.cursors:
            if cursor.y not in line_nums:
                line_nums.append(cursor.y)
                # Reverse string
                editor.lines[cursor.y].data = editor.lines[cursor.y].data[::-1]

module = {
    "class": Reverse,
    "name": "upper",
}
