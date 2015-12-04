"""
Basic logging to delay printing until curses is unloaded.
"""
from __future__ import print_function
import os
import logging
from logging.handlers import BufferingHandler, RotatingFileHandler
import sys


# Define an mix of BufferingHandler and MemoryHandler which store records internally and flush on `close`
# https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.BufferingHandler
# https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.MemoryHandler
class BufferingTargetHandler(BufferingHandler):
    # Set up capacity and target for MemoryHandler
    def __init__(self, capacity, fd_target):
        """
        :param int capacity: Amount of records to store in memory
            https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1161-L1176
        :param object fd_target: File descriptor to write output to (e.g. `sys.stdout`)
        """
        # Call our BufferingHandler init
        super(BufferingTargetHandler, self).__init__(capacity)

        # Save target for later
        self._fd_target = fd_target

    def close(self):
        """Upon `close`, flush our internal info to the target"""
        # Flush our buffers to the target
        # https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1185
        # https://github.com/python/cpython/blob/3.3/Lib/logging/handlers.py#L1241-L1256
        self.acquire()
        try:
            for record in self.buffer:
                msg = self.format(record)
                print(msg, file=self._fd_target)
        finally:
            self.release()

        # Then, run our normal close actions
        super(BufferingTargetHandler, self).close()


# Initialize logging
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.handlers = []

# Generate and configure handlers
log_filepath = os.path.join(os.path.expanduser("~"), ".config", "suplemon", "output.log")
logger_handlers = [
    # Output up to 4MB of records to `~/.config/suplemon/output.log` for live debugging
    # https://docs.python.org/3.3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    # DEV: We use append mode to prevent erasing out logs
    # DEV: We use 1 backup count since it won't truncate otherwise =/
    RotatingFileHandler(log_filepath, mode="a", maxBytes=(4 * 1024 * 1024), backupCount=1),
    # Buffer 64k records in memory at a time
    BufferingTargetHandler(64 * 1024, fd_target=sys.stderr),
]
fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger_formatter = logging.Formatter(fmt)
for logger_handler in logger_handlers:
    logger_handler.setFormatter(logger_formatter)

# Save handlers for our logger
for logger_handler in logger_handlers:
    logger.addHandler(logger_handler)
