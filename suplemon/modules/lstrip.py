from suplemon_module import Module


class LStrip(Module):
    def init(self):
        self.bind_key("kHOM7")  # Used to bind a key to the run-method

    def run(self, app, editor):
        # TODO: move cursors in sync with line contents
        line_nums = editor.get_lines_with_cursors()
        for n in line_nums:
            line = editor.lines[n]
            line.data = line.data.lstrip()

module = {
    "class": LStrip,
    "name": "lstrip",
}
