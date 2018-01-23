# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""


__version__ = "0.2.0"

from .ui import UI

from .logger import logger
from .config.config import ConfigLoader
from .backends.curses import CursesBackend


class App:
    def __init__(self, filenames=None, config_file=None):
        self.debug = 1  # TODO: default to 0
        self.version = __version__
        self.running = 0
        self.logger = logger
        self.logger.debug("App.__init__()")
        self.logger.debug("Filenames: {}".format(filenames))

        self.config = None
        self.config_loader = ConfigLoader()

        self.backend = CursesBackend()
        self.ui = UI(self, self.backend)

    def init(self):
        self.logger.debug("App.init()")

        # Load default config
        if not self.config_loader.init():
            return False

        # Load user config
        self.config = self.config_loader.load_user_config()
        return True

    def run(self):
        self.logger.debug("App.run()")
        self.running = 1

        self.backend.init()
        self.backend.start(self.mainloop)
        self.logger.debug("Backend stopped.")

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
            self.handle_logs()

    def handle_logs(self):
        for logger_handler in self.logger.handlers:
            logger_handler.close()
