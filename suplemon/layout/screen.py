
import random
import logging

from .layout import Size

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

# Default color levels for the color cube
cubelevels = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]
# xterm monochrome colors from dark to light
xterm_monochrome = [16, 232, 233, 234, 235, 236, 237, 238, 239, 240, 59, 241, 242, 243, 244, 102, 245, 246, 247, 248, 145, 249, 250, 251, 252, 188, 253, 254, 255, 231]
# Generate a list of midpoints of the above list
snaps = [(x+y)/2 for x, y in list(zip(cubelevels, [0]+cubelevels))[1:]]


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_xterm(rgb):
    """
    Converts hex color values to the nearest equivalent xterm-256 color.
    """
    r, g, b = rgb
    # Handle monochrome
    if r == g and g == b and r < 256:
        return xterm_monochrome[int((r / 255) * (len(xterm_monochrome)-1))]
    # Using list of snap points, convert RGB value to cube indexes
    r, g, b = map(lambda x: len(tuple(s for s in snaps if s < x)), (r, g, b))
    # Simple colorcube transform
    return r*36 + g*6 + b + 16


color_logger = logging.getLogger("{}.{}".format(__name__, "Color"))


class Color(object):
    def __init__(self, color=None):
        self._xterm256 = None

        if isinstance(color, int):
            self._xterm256 = color

        elif isinstance(color, (list, tuple)):
            self._xterm256 = rgb_to_xterm(color)

        elif isinstance(color, str):
            self._xterm256 = rgb_to_xterm(hex_to_rgb(color))

        elif color is None:
            self._xterm256 = -1

        else:
            raise ValueError("Invalid color value: " + str(color))

        # if color is not None:
        #     color_logger.debug("Color: {} converted to xterm: {}".format(color, self._xterm256))

    def _random(self):
        self._xterm256 = random.randrange(1, 255)


class Style(object):
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
        self._attrs.append(Style.BOLD)

    def set_underline(self):
        self._attrs.append(Style.UNDERLINE)

    def set_blink(self):
        self._attrs.append(Style.BLINK)

    def is_bold(self):
        return Style.BOLD in self._attrs

    def is_underline(self):
        return Style.UNDERLINE in self._attrs

    def is_blink(self):
        return Style.BLINK in self._attrs


class ScreenString(object):
    def __init__(self, text="", fg=None, bg=None, bold=0, underline=0, blink=0):
        self._text = text
        self.style = Style()
        if bold:
            self.style.set_bold()
        if underline:
            self.style.set_underline()
        if blink:
            self.style.set_blink()
        if fg:
            self.style.set_color_fg(Color(fg))  # TODO: decide where to create Color instances
        if bg:
            self.style.set_color_bg(Color(bg))  # TODO: decide where to create Color instances

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def __str__(self):
        return self._text

    def __len__(self):
        return len(self._text)


def get_buffer_line_length(line):
    return sum(map(lambda item: len(item), line))


def normalize_screen_buffer(buffer, size, fill=" "):
    line_count = len(buffer)
    # Cut off excess rows
    if line_count > size[1]:
        buffer = buffer[:size.height]

    # Add missing rows
    elif line_count < size[1]+1:
        buffer = buffer + [[ScreenString(fill*size.width)]] * (size.height - line_count)

    # Normalize line lengths
    for i, line in enumerate(buffer):
        length = get_buffer_line_length(line)

        # Pad lines that are too short
        if length <= size[0]:
            buffer[i] = buffer[i] + [ScreenString(fill * (size[0] - length))]

        # Cut lines that are too long
        if length > size[0]:
            while 1:
                line = buffer[i]
                excess = get_buffer_line_length(line) - size[0]
                # Remove the last segment of the current line if it is shorter than the excess
                if len(buffer[i][-1]) < excess:
                    buffer[i].pop()
                # Otherwise trim the last segment
                else:
                    text = buffer[i][-1].text
                    buffer[i][-1].text = text[:len(text)-excess]
                    excess = 0
                if not excess:
                    break

    return buffer


class Screen(object):
    def __init__(self, buffer=None, size=None):
        if size is None:
            raise ValueError("Screen must have a size")
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__))
        self.size = size if size else Size(0, 0)
        self.buffer = buffer if buffer else [[ScreenString(("X" * self.size.width))]] * self.size.height
        self.buffer = normalize_screen_buffer(self.buffer, size)

    def __repr__(self):
        return "Screen(rows=" + str(len(self.buffer)) + ")"
