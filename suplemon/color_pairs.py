# -*- encoding: utf-8
"""
Manage curses color pairs
"""

import curses
import logging


class ColorPairs:
    def __init__(self):
        self.logger = logging.getLogger(__name__ + "." + ColorPairs.__name__)
        self._colors = dict()

        # color_pair(0) is hardcoded
        # https://docs.python.org/3/library/curses.html#curses.init_pair
        self._color_count = 1

        # dynamic in case terminal does not support use_default_colors()
        self._invalid = curses.COLOR_RED
        self._default_fg = -1
        self._default_bg = -1

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
            index, color, fg, bg, attrs = self._colors[name]
            self.logger.info("Updating exiting color pair with index %i and name '%s'" % (index, name))
        else:
            # Create new color pair
            index = self._color_count
            self.logger.info("Creating new color pair with index %i and name '%s'" % (index, name))
            if index < curses.COLOR_PAIRS:
                self._color_count += 1
            else:
                self.logger.warning(
                    "Failed to create new color pair for " +
                    "'%s', the terminal description for '%s' only supports up to %i color pairs" %
                    (name, curses.termname().decode("utf-8"), curses.COLOR_PAIRS)
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
                (curses.termname().decode("utf-8"), curses.COLORS, color)
            )
            return self._invalid

        return color_i
