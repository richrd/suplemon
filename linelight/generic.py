from helpers import *

#TODO: improve this
def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, ["import", "from"]):
        color = 11
    elif starts(line, "*"):  # List
        color = 12    # Cyan
    elif starts(line, ["#", "/*", "//"]):  # Comment
        color = 13    # Green
    elif starts(line, "<"):    # HTML
        color = 12    # Cyan
    return color