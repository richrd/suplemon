#-*- encoding: utf-8
"""
Base class for extension modules to inherit.
"""
from helpers import *

class Command:
    def __init__(self, app):
        self.app = app
        self.init()

    def init(self):
        pass