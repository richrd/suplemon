
import logging
import suplemon.widgets as widgets
from .screen import Screen, ScreenString


class UI(object):
    def __init__(self, app, backend):
        self.logger = logging.getLogger("{0}.UI".format(__name__))
        self.app = app
        self.backend = backend

        # self.layout_test()
        self.root_widget = widgets.VSplitWidget()
        self.root_widget.add_child(HeaderWidget(app=self.app), 0)
        self.root_widget.add_child(widgets.TestWidget(), 100)
        self.root_widget.add_child(FooterWidget(app=self.app), 0)

    def update(self):
        self.logger.debug("update()")
        input = self.backend.input.get_input()
        key = ""
        if input is None:
            pass
        elif input.is_resize:
            size = self.backend.output.get_size()
            key = "{}".format(size)
        else:
            if input.key == "q":
                self.app.shutdown()
                return
            key = input.key
        self.render(key)

    def render(self, text=""):
        size = self.backend.output.get_size()
        self.root_widget.set_size(size)

        screen = self.root_widget.render()
        self.backend.output.render(screen)

    def layout_test(self):
        hs1 = widgets.HSplitWidget()
        hs1.add_child(widgets.TestWidget(), 50)
        hs1.add_child(widgets.TestWidget(), 25)
        hs1.add_child(widgets.TestWidget(), 25)

        hs2 = widgets.HSplitWidget()
        hs2.add_child(widgets.TestWidget(), 40)
        hs2.add_child(widgets.TestWidget(), 20)
        hs2.add_child(widgets.TestWidget(), 40)

        hs3 = widgets.HSplitWidget()
        hs3.add_child(widgets.TestWidget(), 25)
        hs3.add_child(widgets.TestWidget(), 50)
        hs3.add_child(widgets.TestWidget(), 25)

        hs4 = widgets.HSplitWidget()
        hs4.add_child(widgets.TestWidget(), 40)
        hs4.add_child(widgets.SpacerWidget(), 0)
        hs4.add_child(widgets.SpacerWidget(), 0)
        hs4.add_child(widgets.SpacerWidget(), 0)
        hs4.add_child(widgets.TestWidget(), 20)
        hs4.add_child(widgets.SpacerWidget(), 0)
        hs4.add_child(widgets.TestWidget(), 40)

        vs1 = widgets.VSplitWidget()
        vs1.add_child(widgets.HeaderWidget(), 0)
        vs1.add_child(hs1, 20)
        vs1.add_child(hs2, 30)
        vs1.add_child(widgets.SpacerWidget(), 0)
        vs1.add_child(hs3, 30)
        vs1.add_child(hs4, 20)
        # self.root_widget.set_children([hs1, hs2, hs3, hs4])  # Automatic

        self.root_widget = vs1


class HeaderWidget(widgets.BaseWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def render(self):
        v = self.app.version
        return Screen([[ScreenString("Suplemon v" + v)]])


class FooterWidget(widgets.BaseWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def render(self):
        return Screen([[ScreenString("---")]])
