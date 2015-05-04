#-*- encoding: utf-8
"""
Cursor object for storing cursor data.
"""
    
from collections import namedtuple


_Cursor = namedtuple('Cursor', 'x,y')


class Cursor(_Cursor):
    def __new__(cls, x, y=None):
        if isinstance(x, tuple):
            return _Cursor.__new__(cls, x=x.x, y=x.y)
        return _Cursor.__new__(cls, x, y)
    
    def tuple(self):
        return tuple(self)
