from suplemon_module import Module


class TabsToSpaces(Module):
    def run(self, app, editor):
        i = 0
        for line in editor.lines:
            new = line.data.replace("\t", " "*editor.config["tab_width"])
            editor.lines[i].data = new
            i += 1

module = {
    "class": TabsToSpaces,
    "name": "tabstospaces",
}
