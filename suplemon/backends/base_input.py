
import logging

from .base_backend import AbstractBackend


class InputBackend(AbstractBackend):
    def __init__(self, backend=None):
        super().__init__(backend=backend)
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        if not backend:
            self.logger.debug("no backend in __init__")

    def use_mouse(self, yes=True):
        """Enable or disable mouse input for the backend."""
        self._use_mouse(yes)

    def get_events(self):
        """Get multiple events from the backend if they occur close enough in time."""
        raise NotImplementedError

    def get_input(self):
        """Get a single input event from the backend."""
        raise NotImplementedError
