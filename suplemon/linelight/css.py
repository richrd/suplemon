from helpers import *


class Syntax:
    def get_comment(self):
        return ("/*", "*/")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if starts(line, "@import"):
            color = 4    # Blue
        elif starts(line, "$"):
            color = 2    # Green
        elif starts(line, "/*") or ends(line, "*/"):
            color = 5    # Magenta
        elif starts(line, "{") or ends(line, "}") or ends(line, "{"):
            color = 6    # Cyan
        elif ends(line, ";"):
            color = 3    # Yellow
        return color
