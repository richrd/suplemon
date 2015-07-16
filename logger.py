# -*- encoding: utf-8
"""
Basic logging to delay printing until curses is unloaded.
"""
import time

import helpers
import constants


class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = None
        self.entries = []
        self.labels = {
            constants.LOG_WONTFIX: "WONTFIX",
            constants.LOG_INFO: "INFO",
            constants.LOG_WARNING: "WARNING",
            constants.LOG_ERROR: "ERROR",
        }

    def log(self, data, log_type=None):
        if log_type is None:
            log_type = constants.LOG_ERROR
        self.entries.append((log_type, str(data), time.time()))

    def output(self):
        for entry in self.entries:
            try:
                log_type = self.get_type_str(entry[0])
                stamp = time.strftime("%H:%M:%S", time.localtime(entry[2]))
                print("[" + stamp + " " + log_type + "] " + str(entry[1]))
            except:
                print("Failed to print a log entry and forgot to write it in a file :(")
                print("Here's why:")
                print(helpers.get_error_info())

    def get_type_str(self, log_type):
        if log_type in self.labels.keys():
            return self.labels[log_type]
        return "UNKNOWN"
