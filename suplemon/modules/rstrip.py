# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class RStrip(Module):
    """Trim whitespace from the end of lines."""

    def run(self, app, editor, args):
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.set_data(line.data.rstrip())


module = {
    "class": RStrip,
    "name": "rstrip",
}
