
import logging


class AbstractBackend(object):
    def __init__(self, backend=None):
        self._backend = backend
        self._running = 0
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))

    def init(self, *args):
        """Initialize the backend. This should be called before any other calls to the backend."""
        assert not self._running
        self._init(*args)

    def start(self, *args):
        assert not self._running
        self._running = 1
        self._start(*args)

    def stop(self):
        assert self._running
        self._running = 0
        self._stop()

    def _init(self):
        raise NotImplementedError

    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError


class Backend(AbstractBackend):
    def __init__(self, input, output):
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        self.input = input
        self.output = output
