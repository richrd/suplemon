from mod_base import *

class Upper(Command):
    def run(self, app, editor):
        line_nums = []
        for cursor in editor.cursors:
            if not cursor.y in line_nums:
                line_nums.append(cursor.y)
                editor.lines[cursor.y].data = editor.lines[cursor.y].data.upper()

module = {
    "class": Upper,
    "name": "upper",
}
