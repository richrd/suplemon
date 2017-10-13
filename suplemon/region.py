# -*- encoding: utf-8

"""
Regions for representing cursors and selections.
"""


class Regions(object):
    """
    Collection of regions.
    """

    def __init__(self):
        self.regions = []
        # The 'primary' region. Used for autocomplete dropdown, and for individual cursor manipulation.
        self.current_region = 0

    def move(self, delta=1):
        for reg in self.regions:
            reg.move(delta)


class Region(object):
    """
    A region representing a cursor or selection.
    """

    def __init__(self, start=0, end=0):
        self._start = start  # Start of the selection
        self._end = end      # End of the selection

        # Prefered X coordinate
        # This should be set when explicitly moving on the x-axis
        # If moving vertically the calculated x should be <= _xpos
        self._xpos = None

    @property
    def start(self):
        return min(self._start, self._end)

    @property
    def end(self):
        return max(self._start, self._end)

    def is_region(self):
        return self._start != self._end

    def move(self, delta=0):
        self._start += delta
        self._end += delta

    def move_left(self, delta=1):
        self.move(abs(delta) * -1)

    def move_right(self, delta=1):
        self.move(abs(delta))
