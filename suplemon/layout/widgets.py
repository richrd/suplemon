from wcwidth import wcswidth

from .layout import Size
from .containers import Container
from .screen import Screen, ScreenString
from ..document import Document


class BaseWidget(Container):
    """Base class for all widgets"""
    pass


class TestWidget(BaseWidget):
    """
    Widget displays it's size in the center and borders around its edges (useful for debugging).
    """
    def render(self):
        w, h = self.size

        top = [ScreenString("+NW" + ("-" * (w-6)) + "NE+", fg=1)]
        bottom = [ScreenString("+SW" + ("-" * (w-6)) + "SE+", fg=2)]
        buffer = [top]

        halfwayY = int((h-2) / 2)
        i = 0
        while i < h-2:
            start = ScreenString("|", fg=1)
            end = ScreenString("|", fg=2)
            if i == halfwayY:
                size_str = "{0[0]} x {0[1]}".format(self.size)
                max_w = w - 2
                line = [start, ScreenString(size_str.center(max_w, " "), fg="#333333"), end]
            else:
                line = [start, ScreenString((" " * (w-2))), end]
            buffer.append(line)
            i += 1
        buffer.append(bottom)

        sc = Screen(buffer, self.size)
        return sc


class Spacer(BaseWidget):
    def __init__(self, char="#"):
        super().__init__()
        self.char = char
        self._prefered_size = Size(1, 1)

    def render(self):
        char_count = self.size.width
        line = self.char * char_count
        lines = [[ScreenString(line)]] * self.size.height
        scr = Screen(lines, self.size)
        return scr


class DocumentView(BaseWidget):
    """
    TODO: Document viewer...
    """
    def __init__(self, char="#"):
        super().__init__()
        f = open("./suplemon/layout/widgets.py")
        data = f.read()
        f.close()

        self.document = Document(data)
        self.scroll_y = 0

    def render(self):
        w, h = self.size
        buffer = []
        lines = self.document.lines[self.scroll_y:]
        number_width = len(str(len(lines)))

        """
        TODO:
        - line wrapping
        - highlighting
        - ...
        """
        for i, line in enumerate(lines):
            line_no = i + self.scroll_y + 1
            # Render a single line of the document
            buffer.append([
                ScreenString(
                    str(line_no).rjust(number_width),
                    fg=(60, 60, 60),
                    bg=(20, 20, 20),
                ),
                ScreenString(" ", bg=(20, 20, 20)),
                ScreenString(line),
            ])

        return Screen(buffer, self.size)
