# -*- encoding: utf-8
"""
Line object to represent a single line in the text editor.
"""


class Line:
    def __init__(self, data=""):
        if isinstance(data, Line):
            data = data.data
        self.data = data
        self.x_scroll = 0
        self.state = None

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, v):
        self.data[i] = v

    def __str__(self):
        return self.data

    def __add__(self, other):
        return Line(self.data + other)

    def __radd__(self, other):
        return Line(other + self.data)

    def __len__(self):
        return len(self.data)

    def get_data(self):
        return self.data

    def set_data(self, data):
        if isinstance(data, Line):
            data = data.get_data()
        self.data = data

    def set_state(self, state):
        self.state = state

    def find(self, what, start=0):
        return self.data.find(what, start)

    def strip(self, *args):
        return self.data.strip(*args)

    def reset_state(self):
        self.state = None
