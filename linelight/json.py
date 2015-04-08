from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, ["{", "}"]):
        color = 4    # Blue
    elif starts(line, "\""):
        color = 3    # Green
    return color
