"""
Basic logging to delay printing until curses is unloaded.
"""
import time

from helpers import *

class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = None
        self.entries = []
        self.labels = {
            LOG_WONTFIX: "WONTFIX",
            LOG_INFO: "INFO",
            LOG_WARNING: "WARNING",
            LOG_ERROR: "ERROR",
        }

    def log(self, data, log_type=3):
        self.entries.append( (log_type, str(data), time.time()) )

    def output(self):
        for entry in self.entries:
            try:
                log_type = self.get_type_str(entry[0])
                stamp = time.strftime("%H:%M:%S", time.localtime(entry[2]))
                print("[LOG - " + stamp + " - " + log_type + "]")
                print(entry[1])
            except:
                print("Shit! Failed to print a log entry and forgot to write it in a file :(")
                print("Here's why:")
                print(get_error_info())
            
    def get_type_str(self, log_type):
        if log_type in self.labels.keys():
            return self.labels[log_type]
        return "UNKNOWN"
