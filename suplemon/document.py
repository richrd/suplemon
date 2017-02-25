# -*- encoding: utf-8

"""
Document for immutable text representation.
"""


class Document(object):
    """
    Immutable text representation.
    """

    def __init__(self, text="", newline="\n"):
        self._newline = newline
        self._text = text
        self._lines = None
        self._line_count = None
        self._line_start_indices = None

    def __str__(self):
        return self._text

    def __len__(self):
        return len(self._text)

    @property
    def text(self):
        return self._text

    @property
    def line_count(self):
        if self._line_count is not None:
            return self._line_count
        self._line_count = self._text.count(self._newline)+1
        return self._line_count

    @property
    def lines(self):
        if self._lines is not None:
            return self._lines
        self._lines = self._text.split(self._newline)
        return self._lines

    @property
    def line_start_indices(self):
        # Get cached if available
        if self._line_start_indices is not None:
            return self._line_start_indices

        # Generate cache
        lengths = map(len, [s for s in self._text.split(self._newline)])
        indices = [0]
        pos = 0

        for length in lengths:
            pos += length + len(self._newline)
            indices.append(pos)

        if len(indices) > 1:
            indices.pop()

        self._line_start_indices = indices
        return indices

    def index_to_pos(self, index):
        assert index <= len(self._text)
        if index == 0:
            return 0, 0  # Short circuit

        indices = self.line_start_indices
        row = 0
        prev_line_index = 0
        for line_index in indices:
            if line_index > index:
                break
            prev_line_index = line_index
            row += 1
        row -= 1
        return (row, index-prev_line_index)

    def pos_to_index(self, row, col):
        return self.line_start_indices[row] + col
