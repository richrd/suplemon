# -*- encoding: utf-8

from suplemon_module import Module


class RStrip(Module):
    def init(self):
        self.bind_key("kEND7")  # Used to bind a key to the run-method

    def run(self, app, editor, args):
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.set_data(line.data.rstrip())

module = {
    "class": RStrip,
    "name": "rstrip",
}
