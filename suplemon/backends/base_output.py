
import logging

from .base_backend import AbstractBackend


class OutputBackend(AbstractBackend):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))

    def has_colors(self):
        """Return True if the output has color support."""
        return self._has_colors()

    def render(self, screen):
        """Render a screen to the output."""
        self._render(screen)
