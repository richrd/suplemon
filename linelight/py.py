from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, ["import", "from"]):
        color = 11
    elif starts(line, "class"):
        color = 13    # Green
    elif starts(line, "def"):
        color = 12    # Cyan
    elif starts(line, ["return", "yield"]):
        color = 15    # Red
    elif starts(line, "self."):
        color = 13    # Cyan
    elif starts(line, ["#", "//", "\"", "'"]):
        color = 14    # Magenta
    elif starts(line, ["if", "elif","else", "finally", "try", "except", "for ", "while ", "continue", "pass", "break"]):
        color = 17    # Yellow
    return color