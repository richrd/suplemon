# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""


__version__ = "0.1.90"

from .ui import UI

from .logger import logger
from .backends.curses import CursesBackend


class App:
    def __init__(self, filenames=None, config_file=None):
        self.debug = 1  # TODO: default to 0
        self.version = __version__
        self.running = 0
        self.logger = logger
        self.logger.debug("============================================================")
        self.logger.debug("App.__init__()")
        self.logger.debug("Filenames: {}".format(filenames))

        self.backend = CursesBackend()
        self.ui = UI(self, self.backend)

    def init(self):
        self.logger.debug("App.init()")
        return True

    def run(self):
        self.logger.debug("App.run()")
        self.running = 1

        self.backend.init()
        self.backend.start(self.mainloop)
        self.logger.debug("Backend ended.")

    def mainloop(self):
        self.logger.debug("App.mainloop()")

        self.ui.render()
        while self.running:
            self.ui.update()

        print("App.mainloop() END")

    def shutdown(self):
        self.logger.debug("App.shutdown()")
        self.running = 0
        self.backend.stop()

        if self.debug:
            for logger_handler in self.logger.handlers:
                logger_handler.close()
