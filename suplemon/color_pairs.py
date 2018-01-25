# -*- encoding: utf-8
"""
Manage curses color pairs
"""

import curses
import logging


class ColorManager:
    def __init__(self, app):
        self._app = app
        self.logger = logging.getLogger(__name__ + "." + ColorManager.__name__)
        self._colors = dict()

        # color_pair(0) is hardcoded
        # https://docs.python.org/3/library/curses.html#curses.init_pair
        self._color_count = 1
        self._invalid = curses.COLOR_WHITE if curses.COLORS < 8 else curses.COLOR_RED

        # dynamic in case terminal does not support use_default_colors()
        self._default_fg = -1
        self._default_bg = -1
        self._setup_colors()
        self._load_color_theme()
        self._app.set_event_binding("config_loaded", "after", self._load_color_theme)

    def _setup_colors(self):
        """Initialize color support and define colors."""
        curses.start_color()

        self.termname = curses.termname().decode('utf-8')
        self.logger.info(
            "Currently running with TERM '%s' which provides %i colors and %i color pairs according to ncurses." %
            (self.termname, curses.COLORS, curses.COLOR_PAIRS)
        )

        if curses.COLORS == 8:
            self.logger.info("Enhanced colors not supported.")
            self.logger.info(
                "Depending on your terminal emulator 'export TERM=%s-256color' may help." %
                self.termname
            )
            self._app.config["editor"]["theme"] = "8colors"

        try:
            curses.use_default_colors()
        except:
            self.logger.warning(
                "Failed to load curses default colors. " +
                "You will have no transparency or terminal defined default colors."
            )
            # https://docs.python.org/3/library/curses.html#curses.init_pair
            # "[..] the 0 color pair is wired to white on black and cannot be changed"
            self.set_default_fg(curses.COLOR_WHITE)
            self.set_default_bg(curses.COLOR_BLACK)

    def _load_color_theme(self, *args):
        colors = self._get_config_colors()
        for key in colors:
            values = colors[key]
            self.add_translate(
                key,
                values.get('fg', None),
                values.get('bg', None),
                values.get('attribs', None)
            )
        self._app.themes.use(self._app.config["editor"]["theme"])

    def _get_config_colors(self):
        if curses.COLORS == 8:
            return self._app.config["display"]["colors_8"]
        elif curses.COLORS == 88:
            return self._app.config["display"]["colors_88"]
        elif curses.COLORS == 256:
            return self._app.config["display"]["colors_256"]
        else:
            self.logger.warning(
                "No idea how to handle a color count of %i. Defaulting to 8 colors." % curses.COLORS
            )
            return self._app.config["display"]["colors_8"]

    def set_default_fg(self, color):
        self._default_fg = color

    def set_default_bg(self, color):
        self._default_bg = color

    def _get(self, name, index=None, default=None, log_missing=True):
        ret = self._colors.get(str(name), None)
        if ret is None:
            if log_missing:
                self.logger.warning("Color '%s' not initialized. Maybe some issue with your theme?" % name)
            return default
        if index is not None:
            return ret[index]
        return ret

    # FIXME: evaluate default returns on error. none? exception? ._default_[fb]g? .invalid? hardcoded? pair(0)?
    def get(self, name):
        """ Return colorpair ORed attribs or a fallback """
        return self._get(name, index=1, default=curses.color_pair(0))

    def get_alt(self, name, alt):
        """ Return colorpair ORed attribs or alt """
        return self._get(name, index=1, default=alt, log_missing=False)

    def get_fg(self, name):
        """ Return foreground color as integer """
        return self._get(name, index=2, default=curses.COLOR_WHITE)

    def get_bg(self, name):
        """ Return background color as integer """
        return self._get(name, index=3, default=curses.COLOR_RED)

    def get_color(self, name):
        """ Alternative for get(name) """
        return self.get(name)

    def get_all(self, name):
        """ color, fg, bg, attrs = get_all("something") """
        ret = self._get(name)
        if ret is None:
            return (None, None, None, None)
        return ret[1:]

    def contains(self, name):
        return str(name) in self._colors

    def add_translate(self, name, fg, bg, attributes=None):
        """
            Store or update color definition.
            fg and bg can be of form "blue" or "color162".
            attributes can be a list of attribute names like "bold" or "underline".
        """
        return self.add_curses(
            name,
            self.translate_color(fg, check_for="fg"),
            self.translate_color(bg, check_for="bg"),
            self.translate_attributes(attributes)
        )

    def add_curses(self, name, fg, bg, attrs=0):
        """ Store or update color definition. fg, bg and attrs must be valid curses values """
        # FIXME: catch invalid colors, attrs,...
        name = str(name)
        if name in self._colors:
            # Redefine exiting color pair
            index, color, _fg, _bg, _attrs = self._colors[name]
            self.logger.debug(
                "Updating exiting color pair with index %i, name '%s', fg=%i, bg=%i and attrs=%i" % (
                    index, name, fg, bg, attrs
                )
            )
        else:
            # Create new color pair
            index = self._color_count
            self.logger.debug(
                "Creating new color pair with index %i, name '%s', fg=%i, bg=%i and attrs=%i" % (
                    index, name, fg, bg, attrs
                )
            )
            if index < curses.COLOR_PAIRS:
                self._color_count += 1
            else:
                self.logger.warning(
                    "Failed to create new color pair for " +
                    "'%s', the terminal description for '%s' only supports up to %i color pairs." %
                    (name, self.termname, curses.COLOR_PAIRS)
                )
                color = curses.color_pair(0) | attrs
                self._colors[name] = (0, color, curses.COLOR_WHITE, curses.COLOR_BLACK, attrs)
                return color
        curses.init_pair(index, fg, bg)
        color = curses.color_pair(index) | attrs
        self._colors[name] = (index, color, fg, bg, attrs)
        return color

    def translate_attributes(self, attributes):
        if attributes is None:
            return 0
        val = 0
        for attrib in attributes:
            val |= getattr(curses, "A_" + attrib.upper(), 0)
        return val

    def translate_color(self, color, check_for=None):
        if color is None:
            return self._invalid

        color_i = getattr(curses, "COLOR_" + color.upper(), None)
        if color_i is not None:
            return color_i

        color = color.lower()
        if color == "default":
            # FIXME: what to return if check_for is not set?
            return self._default_fg if check_for == "fg" else self._default_bg
        elif color.startswith("color"):
            color_i = color[len("color"):]
        elif color.startswith("colour"):
            color_i = color[len("colour"):]
        else:
            self.logger.warning("Invalid color specified: '%s'" % color)
            return self._invalid

        try:
            color_i = int(color_i)
        except:
            self.logger.warning("Invalid color specified: '%s'" % color)
            return self._invalid

        if color_i >= curses.COLORS:
            self.logger.warning(
                "The terminal description for '%s' does not support more than %i colors. Specified color was %s" %
                (self.termname, curses.COLORS, color)
            )
            return self._invalid

        return color_i
