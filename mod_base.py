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

    def bind_key(self, key):
        """Shortcut for binding run method to a key."""
        self.app.set_key_binding(key, self._proxy_run)
        
    def _proxy_run(self):
        self.run(self.app, self.app.get_editor())
