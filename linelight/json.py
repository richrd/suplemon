from helpers import *


class Syntax:
    def get_comment(self, line):
        return ("", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if starts(line, ["{", "}"]):
            color = 3    # Blue
        elif starts(line, "\""):
            color = 2    # Green
        return color
