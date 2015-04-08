from helpers import *

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
