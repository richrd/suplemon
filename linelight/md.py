from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, "*"):  # List
        color = 7    # Cyan
    elif starts(line, "#"):  # Header
        color = 3    # Green
    elif starts(line, ">"):  # Item desription
        color = 4    # Yellow
    elif starts(raw_line, "    "):  # Code
        color = 6    # Magenta
    return color
