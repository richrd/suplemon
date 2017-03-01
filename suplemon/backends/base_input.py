
import logging

from .base_backend import AbstractBackend


class InputBackend(AbstractBackend):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))

    def init(self):
        """Initialize the backend. This should be called before any other calls to the backend."""
        raise NotImplementedError

    def use_mouse(self, yes=True):
        """Enable mouse input for the backend."""
        self._use_mouse(yes)

    def get_events(self):
        """Get multiple events from the backend if they occur close enough in time."""
        raise NotImplementedError

    def get_input(self):
        """Get a single input event from the backend."""
        raise NotImplementedError
