# -*- encoding: utf-8

"""
Text handling and manipulation.
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


class Buffer(object):
    """
    Text manipulation.
    """

    def __init__(self, text=""):
        self._newline = "\n"
        self._read_only = False
        self.document = Document(text, self._newline)
        self.regions = []

    def __str__(self):
        return self.document.text

    def _set_text(self, text):
        assert self._read_only is False
        self.document = Document(text, self._newline)

    #
    # Insert / Delete
    #

    def insert_text(self, text, pos):
        text = self.document.text[:pos] + text + self.document.text[pos:]
        return text

    #
    # Transformations
    #

    def transform_lines(self, indices, callback):
        text = self.document.text
        lines = text.split(self._newline)
        for i in indices:
            lines[i] = callback(lines[i])
        return self._newline.join(lines)

    def transform_all_lines(self, callback):
        return self.transform_lines(range(self.document.line_count), callback)

    def transform_region(self, start, end, callback):
        assert start < end
        text = self.document.text
        text = text[:start] + callback(text[start:end]) + text[end:]
        return text


if __name__ == "__main__":
    data = ""
    with open("test_doc") as f:
        data = f.read()

    b = Buffer()
    b._set_text(data)

    print(b)
    print(b.document.lines)
    print(b.document.line_count)
