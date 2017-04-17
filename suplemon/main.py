# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""


__version__ = "0.1.90"


from .logger import logger
from .backends.curses import CursesBackend


class App:
    def __init__(self, filenames=None, config_file=None):
        self.debug = 1
        self.logger = logger
        self.logger.debug("__init__")

        # EXPERIMENTAL
        self.backend = CursesBackend()

    def init(self):
        self.logger.debug("init")
        self.backend.init()
        return True

    def run(self):
        self.logger.debug("run")
        self.backend.start()

    def shutdown(self):
        self.logger.debug("shutdown")
        self.backend.stop()
        self.logger.debug("shutdown")

        if self.debug:
            for logger_handler in self.logger.handlers:
                logger_handler.close()
