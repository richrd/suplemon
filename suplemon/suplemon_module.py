# -*- encoding: utf-8
"""
Base class for extension modules to inherit.
"""

import logging


class Module:
    def __init__(self, app):
        self.app = app
        self.init()

    def init(self):
        """Initialize the module.

        This function is run when the module is loaded and can be
        reimplemented for module specific initializations.
        """
        pass

    def init_logging(self, name):
        """Initialize the module logger (self.logger).

        Should be called before the module uses logging.
        Always pass __name__ as the value to name, for consistency.

        Args:
        :param name: should be specified as __name__
        """
        self.logger = logging.getLogger("module.{0}".format(name))

    def run(self, app, editor, args):
        """This is called each time the module is run.

        Called when command is issued via promt or key binding.

        Args:
        :param app: the app instance
        :param editor: the current editor instance
        """
        pass

    def bind_key(self, key):
        """Shortcut for binding run method to a key.

        Args:
        :param key:
        """
        self.app.set_key_binding(key, self._proxy_run)

    def bind_event(self, event, callback):
        """Bind a callback to be called before event is run.

        If the callback returns True the event will be canceled.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "before", callback)

    def bind_event_before(self, event, callback):
        """Bind a callback to be called before event is run.

        If the callback returns True the event will be canceled.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "before", callback)

    def bind_event_after(self, event, callback):
        """Bind a callback to be called after event is run.

        :param event: The event name
        :param callback: Function to be called
        """
        self.app.set_event_binding(event, "after", callback)

    def _proxy_run(self):
        """Calls the run method with necessary arguments."""
        self.run(self.app, self.app.get_editor(), "")
