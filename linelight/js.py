from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, ["import", "from"]):
        color = 11
#    elif starts(line, "class"):
#        color = 13    # Green
    elif starts(line, "function"):
        color = 12    # Cyan
    elif starts(line, ["return"]):
        color = 15    # Red
    elif starts(line, "this."):
        color = 13    # Cyan
    elif starts(line, ["//", "/*", "*/", "*"]):
        color = 14    # Magenta
    elif starts(line, ["if", "else", "for ", "while ", "continue", "break"]):
        color = 17    # Yellow
    return color