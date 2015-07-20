"""
Basic logging to delay printing until curses is unloaded.
"""
import logging


class LoggingHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.messages = []

    def emit(self, record):
        msg = self.format(record)
        self.messages.append(msg)

    def close(self):
        logging.Handler.close(self)

    def output(self):
        for message in self.messages:
            print(message)
