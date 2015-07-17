# -*- encoding: utf-8
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
        # self.print()
        logging.Handler.close(self)

    def print(self):
        for message in self.messages:
            print(message)
