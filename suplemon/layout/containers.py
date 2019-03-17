import logging
from ..utils import divide_by_percentages, divide_evenly

from .layout import Size
from .screen import Screen, ScreenString


class Container(object):
    """Base class for all containers."""
    def __init__(self, children=[]):
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__))
        self.children = children
        self._prefered_size = Size(1, 1)
        self.size = Size()

    def set_size(self, size):
        self.size = size

    def set_children(self, children):
        self.children = children

    @property
    def prefered_size(self):
        return self._prefered_size

    @prefered_size.getter
    def prefered_size(self):
        return self._prefered_size

    def render(self):
        raise NotImplementedError


class _SplitContainer(Container):
    """Base for widgets that display children stacked horizontally or verticaly.

    Each child should either have a percentage, or 0 to let the widget influence its own size.
    """
    def __init__(self, children=[]):
        super().__init__(children=[])
        self.percentages = []
        self.set_children(children)
        self.axis = None  # 0 for X, 1 for Y

    def set_children(self, children):
        if not children:
            self.children = []
            self.percentages = []
            return

        if isinstance(children[0], (list, tuple)):
            # If percentages are provided, use them
            self.children = list(map(lambda item: item[0], children))
            self.percentages = list(map(lambda item: item[1], children))
        else:
            # If percentages aren't provided clear them
            self.children = children
            self.percentages = []

    def add_child(self, child, percentage):
        """Append a widget of percentage size to the layout. If percentage is falsy, the widget determines its size."""
        self.children.append(child)
        self.percentages.append(percentage)

    def set_size(self, size):
        super().set_size(size)
        # If no children exist, do nothing
        if not self.children:
            return

        remaining_size = size[self.axis]  # determine by subtracting fixed widgets from max

        # If children exist but percentages don't then divide the children evenly
        if not self.percentages:
            sizes = divide_evenly(remaining_size, len(self.children))
            for i, child in enumerate(self.children):
                item_size = Size()
                item_size[self.axis] = sizes[i]
                item_size[not self.axis] = size[not self.axis]
                child.set_size(item_size)
            return

        # Find the total of the prefered sizes of children
        prefered_total = 0
        for i, p in enumerate(self.percentages):
            child = self.children[i]
            if not p:
                prefered_total += child.prefered_size[self.axis]
                child.set_size(child.prefered_size)

        remaining_size -= prefered_total

        # Sizes for each child, 0 means use prefered size
        sizes = divide_by_percentages(remaining_size, self.percentages)

        for i, item in enumerate(sizes):
            prefered_size = self.children[i].prefered_size
            item_size = Size()
            if item:
                item_size[self.axis] = sizes[i]
            else:
                item_size[self.axis] = prefered_size[self.axis]
            item_size[not self.axis] = size[not self.axis]
            self.children[i].set_size(item_size)

    def render(self):
        if not self.children:
            return Screen([[ScreenString(" "*self.size.width)]]*self.size.height)

        buffer = []
        if self.axis == 0:
            screens = []
            for child in self.children:
                screens.append(child.render())
            i = 0
            while i < self.size.height:
                joined = []
                for screen in screens:
                    joined = joined + screen.buffer[i]
                buffer.append(joined)
                i += 1
        else:
            for c in self.children:
                buffer += c.render().buffer
        scr = Screen(buffer, self.size)
        return scr


class HSplit(_SplitContainer):
    def __init__(self, children=[]):
        super().__init__(children=children)
        self.axis = 0


class VSplit(_SplitContainer):
    def __init__(self, children=[]):
        super().__init__(children=children)
        self.axis = 1


# USE: Autocomplete menu, sublime style CTRL+P menu etc
class FloatContainer(Container):
    def __init__(self, children=[]):
        super().__init__()
        # TODO: Implement
