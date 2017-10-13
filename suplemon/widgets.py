import logging

from .utils import divide
from .screen import Screen, ScreenString


class BaseWidget(object):
    """Base class for all widgets"""
    def __init__(self):
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__))
        self.size = [0, 0]
        self.min_size = [1, 1]

    def set_size(self, size):
        self.size = size

    def render(self):
        raise NotImplementedError


class TestWidget(BaseWidget):
    """
    Widget with a border around its edges and displays it's size in the center (useful for debugging).
    """
    def render(self):
        w, h = self.size
        top = [ScreenString("+NW" + ("-" * (w-6)) + "NE+")]
        bottom = [ScreenString("+SW" + ("-" * (w-6)) + "SE+")]
        lines = [top]

        halfwayY = int((h-2) / 2)
        i = 0
        while i < h-2:
            if i == halfwayY:
                size_str = "{0[0]} x {0[1]}".format(self.size)
                max_w = w - 2
                line = [ScreenString("|" + size_str.center(max_w, " ") + "|")]
            else:
                line = [ScreenString("|" + (" " * (w-2)) + "|")]
            lines.append(line)
            i += 1
        lines.append(bottom)

        sc = Screen(lines)
        return sc


class SpacerWidget(BaseWidget):
    def render(self):
        char = "#"
        lines = []
        if self.size[0] > self.size[1]:
            lines.append([ScreenString(char * self.size[0])])
        else:
            lines = [[ScreenString(char)]] * self.size[1]
        scr = Screen(lines)
        return scr


class BaseContainerWidget(BaseWidget):
    """Base for widgets that have child widgets."""
    def __init__(self):
        super().__init__()
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class BaseSplitWidget(BaseContainerWidget):
    """Base for widgets that display children stacked horizontally or verticaly.

    Each child must have a percentage specified. To specify a fixed size widget set percentage to 0.
    """
    def __init__(self):
        super().__init__()
        self.percentages = []
        self.axis = 0  # 0 for X, 1 for Y

    def add_child(self, child, percentage):
        """Append a widget of percentage size to the layout. If percentage is falsy, the widget determines its size."""
        super().add_child(child)
        self.percentages.append(percentage)

    def set_size(self, size):
        super().set_size(size)
        i = 0
        remaining_size = size[self.axis]  # determine by subtracting fixed widgets from max
        for p in self.percentages:
            if not p:
                remaining_size -= self.children[i].min_size[self.axis]
            i += 1

        sizes = divide(remaining_size, self.percentages)
        i = 0
        for item in sizes:
            s = [None, None]
            if item:
                s[self.axis] = sizes[i]
            else:
                s[self.axis] = 1
            s[not self.axis] = size[not self.axis]
            self.children[i].set_size(s)
            i += 1

    def set_children(self, children):
        if not self.percentages:
            for child in children:
                self.percentages.append(100 / len(children))
        self.children = children

    def render(self):
        lines = []
        if self.axis == 0:
            screens = []
            for child in self.children:
                screens.append(child.render())
            i = 0
            while i < self.size[1]:
                joined = []
                for screen in screens:
                    joined = joined + screen.lines[i]
                lines.append(joined)
                i += 1
        else:
            for c in self.children:
                lines += c.render().lines
        scr = Screen(lines)
        return scr


class HSplitWidget(BaseSplitWidget):
    def __init__(self):
        super().__init__()
        self.axis = 0


class VSplitWidget(BaseSplitWidget):
    def __init__(self):
        super().__init__()
        self.axis = 1
