# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class TabsToSpaces(Module):
    """Convert tab characters to spaces in the entire file."""

    def run(self, app, editor, args):
        for i, line in enumerate(editor.lines):
            new = line.data.replace("\t", " "*editor.config["tab_width"])
            editor.lines[i].set_data(new)


module = {
    "class": TabsToSpaces,
    "name": "tabstospaces",
}
