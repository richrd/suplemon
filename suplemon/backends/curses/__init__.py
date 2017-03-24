
import os
import time

from ..base_backend import Backend
from ...screen import Color, ScreenAttributes, ScreenString, Screen


from .curses_input import CursesInput
from .curses_output import CursesOutput


class CursesBackend(Backend):
    def __init__(self):
        self.input, self.output = CursesInput(self), CursesOutput(self)
        super().__init__(self.input, self.output)
        self._root = None  # Root window
        self._escdelay = 25
        self._running = 0
        self.screen = Screen()
        self.screen.lines = [[ScreenString()]]

    def init(self):
        global curses
        # Set ESC detection time
        os.environ["ESCDELAY"] = str(self._escdelay)
        # Now import curses, otherwise ESCDELAY won't have any effect
        import curses
        self.logger.debug("Loaded curses {0}".format(curses.version.decode()))
        self.input.init()
        self.output.init()

    def _start(self):
        """Start curses."""
        curses.wrapper(self.run_wrapped)

    def _stop(self):
        """Unload curses."""
        self._running = 0
        try:
            curses.endwin()
        except:
            self.logger.exception("Failed to shutdown curses.")

    #
    # Curses Specifics
    #

    def run_wrapped(self, *args):
        """Setup curses."""
        self._running = 1
        # Log the terminal type
        termname = curses.termname().decode("utf-8")
        self.logger.debug("Loading UI for terminal: {0}".format(termname))

        self._root = curses.initscr()

        curses.raw()
        curses.noecho()

        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            # curses.curs_set(0)
            pass
        except:
            self.logger.debug("curses.curs_set(0) failed!")

        self.output._set_root(self._root)
        self.input._set_root(self._root)
        self.output.start()
        self.input.start()

        self.run_event_loop()

    def run_event_loop(self):
        """
        Currently this is just a mockup for testing the screen.
        """
        size = self.output.get_size()
        # self.output._
        # self.screen.lines[0][0] = ScreenString(str(time.ctime()) + " – " + str(size))
        self.output.render(self.screen)
        while self._running:
            input = self.input.get_input()
            if input is None:
                pass
            else:
                if input.key == "q":
                    self.stop()
            size = self.output.get_size()
            fg = Color()
            self.screen.lines = []
            y = 0
            while y < size[1]:
                s = ScreenString(str(y) + "." * (size[0]-len(str(y))-1) )
                self.screen.lines.append([s])
                y += 1
            #if input is not None:
            #    self.screen.lines.append([ScreenString(input.to_string()*5, fg=fg)])
            #if self.screen.get_size()[1] > self.output.get_size()[1]-1:
            #    self.screen.lines.pop(0)
            #self.screen.lines[0][0] = ScreenString(str(time.ctime()) + " – " + str(size) + " - " + str(fg._xterm256), fg=fg)
            self.output.render(self.screen)
