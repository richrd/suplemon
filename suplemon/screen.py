
import random

"""
Screen

Screen contains a grid of characters for rendering in terminals.

The screen has a number of lines and columns.
Each line is a list of strings accompanied by a set of attributes.
The cumulative length of all strings on a line shoudln't be greater than the column count.
NOTE: The length must take wide characters into account.

Attributes are:
    - color:
        - background (rgb)
        - foreground (rgb)
    - styles:
        - standout
        - underline
        - bold
        - blink
        - italics
        - ? inverse

"""


class Color(object):
    def __init__(self):
        self._xterm256 = -1
        self._random()

    def _random(self):
        self._xterm256 = random.randrange(1, 255)


class ScreenAttributes(object):
    BOLD = 1
    UNDERLINE = 2
    BLINK = 3

    def __init__(self):
        self._attrs = []
        self._color_bg = Color()
        self._color_fg = Color()

    def set_color_fg(self, fg):
        self._color_fg = fg

    def set_color_bg(self, bg):
        self._color_bg = bg

    def set_bold(self):
        self._attrs.append(ScreenAttributes.BOLD)

    def set_underline(self):
        self._attrs.append(ScreenAttributes.UNDERLINE)

    def set_blink(self):
        self._attrs.append(ScreenAttributes.BLINK)

    def is_bold(self):
        return ScreenAttributes.BOLD in self._attrs

    def is_underline(self):
        return ScreenAttributes.UNDERLINE in self._attrs

    def is_blink(self):
        return ScreenAttributes.BLINK in self._attrs


class ScreenString(object):
    def __init__(self, text="", bold=0, underline=0, blink=0, fg=None, bg=None):
        self._text = text
        self.attributes = ScreenAttributes()
        if bold:
            self.attributes.set_bold()
        if underline:
            self.attributes.set_underline()
        if blink:
            self.attributes.set_blink()
        if fg:
            self.attributes.set_color_fg(fg)
        if bg:
            self.attributes.set_color_bg(bg)

    def __str__(self):
        return self._text

    def __len__(self):
        return len(self._text)


class Screen(object):
    def __init__(self, lines=[]):
        self.lines = lines

    def get_size(self):
        # TODO: Get max x width
        return (1, len(self.lines))
