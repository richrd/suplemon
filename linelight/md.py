from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, "*"):  # List
        color = 12    # Cyan
    elif starts(line, "#"):  # Header
        color = 13    # Green
    elif starts(line, ">"):  # Item desription
        color = 17    # Yellow
    elif starts(raw_line, "    "):  # Code
        color = 14    # Magenta
    return color