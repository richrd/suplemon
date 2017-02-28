
import logging


class AbstractBackend(object):
    def __init__(self):
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        self._running = 0

    def start(self):
        if not self._running:
            self._running = 1
            self._start()

    def stop(self):
        if self._running:
            self._running = 0
            self._stop()

    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError


class Backend(AbstractBackend):
    def __init__(self, input, output):
        self.logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        self.input = input
        self.output = output
