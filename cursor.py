#-*- encoding: utf-8
"""
Cursor object for storing cursor data.
"""

class Cursor:
    def __init__(self, x=0, y=0):
        if type(x) == type((0,)):
            x,y = x
        self.x = x
        self.y = y
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

    def __setitem__(self, i, v):
        if i == 0:
            self.x = v
        elif i == 1:
            self.y = v

    def __eq__(self, item):
        if isinstance(item, Cursor):
            if item.x == self.x and item.y == self.x:
                return True
        return False

    def __ne__(self, item):
        if isinstance(item, Cursor):
            if item.x != self.x and item.y != self.x:
                return False

    def tuple(self):
        return (self.x, self.y)

