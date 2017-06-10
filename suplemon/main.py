# -*- encoding: utf-8

"""
The main class that starts and runs Suplemon.
"""


__version__ = "0.1.90"


from .logger import logger
from .backends.curses import CursesBackend
from .screen import Screen, ScreenString


class App:
    def __init__(self, filenames=None, config_file=None):
        self.debug = 1  # TODO: default to 0
        self.running = 0
        self.logger = logger
        self.logger.debug("============================================================")
        self.logger.debug("App.__init__()")

        # EXPERIMENTAL
        self.backend = CursesBackend()

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
        while self.running:
            input = self.backend.input.get_input()
            key = ""
            if input is None:
                pass
            else:
                if input.key == "q":
                    self.shutdown()
                    break
                key = input.key
            sc = Screen([[ScreenString("Key: " + key)]])
            self.backend.output.render(sc)
        print("App.mainloop() END")

    def shutdown(self):
        self.logger.debug("App.shutdown()")
        self.running = 0
        self.backend.stop()

        if self.debug:
            for logger_handler in self.logger.handlers:
                logger_handler.close()
