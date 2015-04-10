from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, "@import"):
        color = 5
    elif starts(line, "$"):
        color = 3
    elif starts(line, "/*") or ends(line, "*/"):
        color = 6    # Magenta
    elif starts(line, "{") or ends(line, "}") or ends(line, "{"):
        color = 7    # Cyan
    elif ends(line, ";"):
        color = 4    # Yellow
    return color
