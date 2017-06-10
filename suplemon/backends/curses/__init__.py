import os
import time

from ..base_backend import Backend
from ...screen import Color, ScreenAttributes, ScreenString, Screen


from .curses_input import CursesInput
from .curses_output import CursesOutput


class CursesBackend(Backend):
    def __init__(self):
        super().__init__(CursesInput(self), CursesOutput(self))
        self._root = None  # Root window
        self._escdelay = 25
        self._running = 0
        self._callback = None

    def _init(self):
        self.logger.debug("CursesBackend._init()")
        global curses
        # Set ESC detection time
        os.environ["ESCDELAY"] = str(self._escdelay)
        # Now import curses, otherwise ESCDELAY won't have any effect
        import curses
        self.logger.debug("Loaded curses {0}".format(curses.version.decode()))
        self.input.init(curses)
        self.output.init(curses)

    def _start(self, callback=None):
        """Start curses."""
        self.logger.debug("CursesBackend._start()")
        self._callback = callback
        curses.wrapper(self.run_wrapped)

    def _stop(self):
        """Unload curses."""
        self.logger.debug("CursesBackend._stop()")

        self.input.stop()
        self.output.stop()

        try:
            curses.endwin()
        except:
            self.logger.exception("Failed to shutdown curses.")

    def run_wrapped(self, *args):
        """Run input and output."""
        self.logger.debug("CursesBackend.run_wrapped()")

        # Log the terminal type
        termname = curses.termname().decode("utf-8")
        self.logger.debug("Loading UI for terminal: {0}".format(termname))

        self._root = args[0]  # Curses root window

        self.output.start()
        self.input.start()

        if self._callback():
            self._callback()
