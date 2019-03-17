
from ..base_output import OutputBackend


class CursesOutput(OutputBackend):
    def _init(self, curses):
        self.curses = curses
        self._max_pairs = None
        self._colors_enabled = False
        self._last_color_pair = -1
        self._color_pairs = {}

    def _start(self):
        assert self._backend._root is not None
        self.size = self._update_size()
        self.logger.debug(self.size)
        self._start_colors()
        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            self.curses.curs_set(0)
        except:
            self.logger.warning("Hiding default cursor failed!")

    def _update_size(self):
        y, x = self._backend._root.getmaxyx()
        self.size = x, y
        return x, y

    def _start_colors(self):
        if self.curses.can_change_color():
            self._setup_colors()
        else:
            self.curses.use_default_colors()
            self.logger.debug("Term doesn't support changing colors.")

    def _setup_colors(self):
        self._colors_enabled = True
        self.logger.debug("Term supports changing colors.")
        self._max_pairs = self.curses.COLOR_PAIRS
        self.logger.debug("Max color pairs:{}".format(self.curses.COLOR_PAIRS))
        self.curses.start_color()
        self.curses.use_default_colors()

    def _has_colors(self):
        return self._colors_enabled

    def _test_color_pairs_overflow(self):
        """
        Try to initialize more than the maximum amount of colors curses supports (256).
        Used for testing purpouses.
        """
        i = 0
        while i < 300:
            self.logger.debug("Initing color #{}".format(i))
            try:
                self.curses.init_pair(i, 6, 100)
            except:
                self.logger.debug("Failed for #{}".format(i))
                break
            i += 1

    def _stop(self):
        pass

    def _get_color_pair_from_xterm(self, xterm_fg, xterm_bg):
        # Get or initialize a curses color pair based on the xterm equivalents
        # None is returned if the requested color can't be initialized
        # NOTE: A maximum of 256 distinct color pairs can be initialized.
        #       Any colors after that are simply ignored.
        #       It's unlikely that the limit is reached in normal circumstances.
        if not self._colors_enabled:
            return None

        key = (xterm_fg, xterm_bg)
        if key in self._color_pairs.keys():
            return self._color_pairs[key]

        current_color_pair = self._last_color_pair + 1
        try:
            self.curses.init_pair(current_color_pair, key[0], key[1])
            self._last_color_pair = current_color_pair
        except self.curses.error:
            # Can't init color pair
            return None
        curs_color = self.curses.color_pair(self._last_color_pair)
        self._color_pairs[key] = curs_color
        return curs_color

    def _get_color_pair_from_attrs(self, attr):
        return self._get_color_pair_from_xterm(attr._color_fg._xterm256, attr._color_bg._xterm256)

    def _convert_scr_attr(self, attr):
        curses_attr = self.curses.A_NORMAL
        if attr.is_bold():
            curses_attr = curses_attr | self.curses.A_BOLD
        if attr.is_underline():
            curses_attr = curses_attr | self.curses.A_UNDERLINE
        if attr.is_blink():
            curses_attr = curses_attr | self.curses.A_BLINK

        if attr._color_bg._xterm256 or attr._color_bg._xterm256:
            color = self._get_color_pair_from_attrs(attr)
            if color:
                curses_attr = curses_attr | color
        return curses_attr

    def _erase(self):
        self._backend._root.erase()
        # self._backend._root.clear()

    def _render(self, screen):
        # TODO: Warn if screen is bigger than terminal
        if not screen.buffer:
            return False
        self._erase()  # TODO: clear or erase?
        self._backend._root.move(0, 0)
        x = 0
        y = 0
        for item in screen.buffer:
            for part in item:
                attrs = self._convert_scr_attr(part.style)
                self.__addstr(y, x, str(part), attrs)
                x += len(part)
            y += 1
            x = 0
        self._backend._root.refresh()

    def __addstr(self, y, x, s, attrs):
        # Curses addstr needs to be wrapped since it stupidly
        # freaks out whenever writing to bottom right corner.
        # Verified on Python 3.5.2
        # Ref: https://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses

        try:
            self._backend._root.addstr(y, x, str(s), attrs)
        except self.curses.error:
            pass  # Just meh
