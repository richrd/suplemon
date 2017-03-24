
from ..base_output import OutputBackend

curses = None


class CursesOutput(OutputBackend):
    def init(self):
        global curses
        if not curses:
            import curses
        self._root = None
        self._max_pairs = None
        self._colors = False

    def _start(self):
        assert self._root is not None
        self.size = self._update_size()
        self.logger.debug(self.size)
        self._start_colors()
        curses.raw()
        curses.noecho()
        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            curses.curs_set(0)
        except:
            self.logger.warning("curses.curs_set(0) failed!")

    def _update_size(self):
        y, x = self._root.getmaxyx()
        self.size = x, y
        return x, y

    def _start_colors(self):
        if curses.can_change_color():
            self.logger.debug("Term supports changing colors.")
            self._max_pairs = curses.COLOR_PAIRS
            self.logger.debug("Max color pairs:{}".format(curses.COLOR_PAIRS))
            curses.start_color()
            curses.use_default_colors()
            self._setup_colors()
        else:
            self.logger.debug("Term doesn't support changing colors.")

    def _setup_colors(self):
        #                id,  fg,  bg
        # curses.init_pair(10,  -1, -1) # -1 = default!
        curses.init_pair(10,  200, -1)

    def _has_colors(self):
        return curses.has_colors()

        # Test COLOR_PAIRS overflow
        # Only id's 1-256 work
        # Maybe we'll just ignore new colors if 256 would be exceded

        # i = 0
        # while i < 300:
        #     self.logger.debug("Initing color #{}".format(i))
        #     try:
        #         curses.init_pair(i, 6, 100)
        #     except:
        #         self.logger.debug("Failed for #{}".format(i))
        #         break
        #     i += 1

    def _stop(self):
        pass

    def _set_root(self, root):
        self._root = root

    def _convert_scr_attr(self, attr):
        attrs = curses.A_NORMAL
        if attr.is_bold():
            attrs = attrs | curses.A_BOLD
        if attr.is_underline():
            attrs = attrs | curses.A_UNDERLINE
        if attr.is_blink():
            attrs = attrs | curses.A_BLINK
        return attrs

    def _erase(self):
        self._root.erase()
        # self._root.clear()

    def _render(self, screen):
        self._erase()
        self._root.move(0, 0)
        x = 0
        y = 0
        # curses.init_pair(10, -1, screen.lines[0][0].attributes._color_fg._xterm256, -1)
        curses.init_pair(10, -1, screen.lines[0][0].attributes._color_fg._xterm256)
        for line in screen.lines:
            for part in line:
                #if len(part) > self.size[0]:
                #    continue
                attrs = self._convert_scr_attr(part.attributes)
                attrs = attrs | curses.color_pair(10)
                self.__addstr(y, x, str(part), attrs)
                x += len(part)
            y += 1
            x = 0
        self._root.refresh()

    def __addstr(self, y, x, s, attrs):
        try:
            self._root.addstr(y, x, str(s), attrs)
        except curses.error:
            self.logger.exception("__addstr failed!")
            self.logger.warning("size:{}, x,y = {}, len:{}".format(self.size, (x, y), len(s)))
