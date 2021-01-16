# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class InputTest(Module):
    """
    Input event testing utility.
    """

    def handler(self, prompt, event):
        self.app.set_status("InputEvent:" + str(event))
        prompt.on_ready()
        return True  # Disable normal key handling

    def run(self, app, editor, args):
        app.ui.query_filtered("Waiting for input...", handler=self.handler)


module = {
    "class": InputTest,
    "name": "input_test",
}
