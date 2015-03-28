from helpers import *

def parse(raw_line):
    color = 0
    line = raw_line.strip()
    if starts(line, "@import"):
        color = 11
    elif starts(line, "/*") or ends(line, "*/"):
        color = 14    # Magenta
    elif starts(line, "{") or ends(line, "}") or ends(line, "{"):
        color = 12    # Cyan
    elif ends(line, ";"):
        color = 17    # Yellow
    return color