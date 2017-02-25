# -*- encoding: utf-8

"""
Buffer for Document handling and manipulation.
"""

from document import Document


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
