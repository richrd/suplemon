from helpers import *

"""
curses.init_pair(0, curses.COLOR_WHITE, black)
curses.init_pair(1, curses.COLOR_BLACK, black)
curses.init_pair(2, curses.COLOR_RED, black)
curses.init_pair(3, curses.COLOR_GREEN, black)
curses.init_pair(4, curses.COLOR_YELLOW, black)
curses.init_pair(5, curses.COLOR_BLUE, black)
curses.init_pair(6, curses.COLOR_MAGENTA, black)
curses.init_pair(7, curses.COLOR_CYAN, black
"""

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, ["import", "from"]):
        color = 5
    elif starts(line, "class"):
        color = 3    # Green
    elif starts(line, "def"):
        color = 7    # Cyan
    elif starts(line, ["return", "yield"]):
        color = 2    # Red
    elif starts(line, "self."):
        color = 7    # Cyan
    elif starts(line, ["#", "//", "\"", "'"]):
        color = 6    # Magenta
    elif starts(line, ["if", "elif","else", "finally", "try", "except", "for ", "while ", "continue", "pass", "break"]):
        color = 4    # Yellow
    return color