# -*- encoding: utf-8
"""
Various helper constants and functions.
"""

import os
import re
import sys
import time
import traceback


def curr_time():
    """Current time in %H:%M"""
    return time.strftime("%H:%M")


def curr_time_sec():
    """Current time in %H:%M:%S"""
    return time.strftime("%H:%M:%S")


def multisplit(data, delimiters):
    pattern = "|".join(map(re.escape, delimiters))
    return re.split(pattern, data)


def get_error_info():
    """Return info about last error."""
    msg = "{0}\n{1}".format(str(traceback.format_exc()), str(sys.exc_info()))
    return msg


def get_string_between(start, stop, s):
    """Search string for a substring between two delimeters. False if not found."""
    i1 = s.find(start)
    if i1 == -1:
        return False
    s = s[i1 + len(start):]
    i2 = s.find(stop)
    if i2 == -1:
        return False
    s = s[:i2]
    return s


def whitespace(line):
    """Return index of first non whitespace character on a line."""
    i = 0
    for char in line:
        if char != " ":
            break
        i += 1
    return i


def parse_path(path):
    """Parse a relative path and return full directory and filename as a tuple."""
    if path[:2] == "~" + os.sep:
        p = os.path.expanduser("~")
        path = os.path.join(p+os.sep, path[2:])
    ab = os.path.abspath(path)
    parts = os.path.split(ab)
    return parts


def get_filename_cursor_pos(name):
    default = {
        "name": name,
        "row": 0,
        "col": 0,
    }

    m = re.match(r"(.*?):(\d+):?(\d+)?", name)

    if not m:
        return default

    groups = m.groups()
    if not groups[0]:
        return default

    return {
        "name": groups[0],
        "row": abs(int(groups[1])-1) if groups[1] else 0,
        "col": abs(int(groups[2])-1) if groups[2] else 0,
    }
