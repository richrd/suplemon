# -*- encoding: utf-8

import time

import logging
from suplemon.layout.containers import HSplit, VSplit
from suplemon.layout.widgets import BaseWidget, TestWidget, Spacer, DocumentView
from suplemon.layout.screen import Screen, ScreenString
from suplemon.layout.layout import Size


class UI(object):
    def __init__(self, app, backend):
        self.logger = logging.getLogger("{0}.UI".format(__name__))
        self.app = app
        self.backend = backend

        # self.setup_layout()

        # Layout test can be used instead of setup_layout to test a more complex layout
        self.layout_test()

    def setup_layout(self):
        self.root_container = VSplit()
        # self.root_container.add_child(HeaderWidget(app=self.app), 0)
        self.root_container.add_child(TestWidget(), 100)
        # self.footer_widget = FooterWidget(app=self.app)
        self.root_container.add_child(self.footer_widget, 0)

    def update(self):
        input = self.backend.input.get_input()
        key = ""
        if input is None:
            pass
        elif input.is_resize:
            size = self.backend.output.get_size()
            key = "Resize: {}".format(size)
        else:
            if input.key == "q":
                self.app.shutdown()
                return
            key = input.key
        self.render(key)

    def render(self, text=""):
        w, h = self.backend.output.get_size()
        self.root_container.set_size(Size(w, h))

        if text:
            self.footer_widget._set_text(text)
        screen = self.root_container.render()
        self.backend.output.render(screen)

    def layout_test(self):
        # Top row test widgets
        hs1 = HSplit([
            (TestWidget(), 50),
            (TestWidget(), 25),
            (TestWidget(), 25),
        ])

        # Bottom row test widgets
        hs2 = HSplit([
            (TestWidget(), 40),
            (TestWidget(), 10),
            (TestWidget(), 25),
            (TestWidget(), 25),
        ])

        doc_view = DocumentView()

        doc_and_sidebar = HSplit([
            (doc_view, 75),
            (TestWidget(), 25),
        ])

        right_column = VSplit([
            (hs1, 20),
            (doc_and_sidebar, 60),
            (hs2, 20),
        ])

        horizontal_l1 = HSplit([
            (TestWidget(), 20),
            (right_column, 80),
        ])

        self.footer_widget = FooterWidget(app=self.app)

        root = VSplit([
            (HeaderWidget(app=self.app), 0),
            (horizontal_l1, 100),
            (self.footer_widget, 0),
        ])

        # TODO: Verify automatic layout works with static sized widgets (e.g. footer widget)
        # self.root_container.set_children([hs1, hs2, widgets.Spacer(), hs3, hs4, self.footer_widget])  # Automatic

        self.root_container = root


class HeaderWidget(BaseWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def render(self):
        v = self.app.version
        t = time.strftime("%H:%M:%S", time.localtime())
        return Screen([[ScreenString("Suplemon v{} {}".format(v, t))]], self.size)


class FooterWidget(BaseWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._text = ""

    # DEBUG: used for showing last keypress
    def _set_text(self, text):
        self._text = text

    def render(self):
        return Screen([[ScreenString("LAST KEY:" + self._text)]], self.size)
