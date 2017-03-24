
import logging

from .base_backend import AbstractBackend


class OutputBackend(AbstractBackend):
    def __init__(self, backend=None):
        super().__init__()
        self._backend = backend
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        self.size = (0, 0)

    def init(self):
        """Initialize the backend. This should be called before any other calls to the backend."""
        raise NotImplementedError

    def has_colors(self):
        """Return True if the output has color support."""
        return self._has_colors()

    def set_size(self, x, y):
        self.size = (x, y)

    def get_size(self):
        return self.size

    def update_size(self):
        return self._update_size()

    def render(self, screen):
        """Render a screen to the output."""
        self._render(screen)
