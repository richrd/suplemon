from suplemon_module import Module


class Save(Module):
    def run(self, app, editor):
        return app.save_file()

module = {
    "class": Save,
    "name": "save",
}
