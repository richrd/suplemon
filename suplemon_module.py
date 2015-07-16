# -*- encoding: utf-8
"""
Base class for extension modules to inherit.
"""


class Module:
    def __init__(self, app):
        self.app = app
        self.init()

    def init(self):
        pass

    def run(self, app, editor):
        pass

    def log(self, data):
        self.app.log(data)

    def bind_key(self, key):
        """Shortcut for binding run method to a key."""
        self.app.set_key_binding(key, self._proxy_run)

    def bind_event(self, event, callback):
        """Binding a method to an event."""
        self.app.set_event_binding(event, "before", callback)

    def bind_event_before(self, event, callback):
        """Binding a method to an event."""
        self.app.set_event_binding(event, "before", callback)

    def bind_event_after(self, event, callback):
        """Binding a method to an event."""
        self.app.set_event_binding(event, "after", callback)

    def _proxy_run(self):
        self.run(self.app, self.app.get_editor())
