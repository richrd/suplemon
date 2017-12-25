# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class SortLines(Module):
    """
    Sort current lines.

    Sorts alphabetically by default.
    Add 'length' to sort by length.
    Add 'reverse' to reverse the sorting.
    """

    def sort_normal(self, line):
        return line.data

    def sort_length(self, line):
        return len(line.data)

    def run(self, app, editor, args):
        args = args.lower()

        sorter = self.sort_normal
        reverse = True if "reverse" in args else False
        if "length" in args:
            sorter = self.sort_length

        indices = editor.get_lines_with_cursors()
        lines = [editor.get_line(i) for i in indices]

        sorted_lines = sorted(lines, key=sorter, reverse=reverse)

        for i, line in enumerate(sorted_lines):
            editor.lines[indices[i]] = line


module = {
    "class": SortLines,
    "name": "sort_lines",
}
