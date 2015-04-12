from helpers import *

class Syntax:
    def get_comment(self, line):
        return ("","")

    def get_color(self, raw_line):
        color = 0
        line = raw_line.strip()
        if starts(line, ["{", "}"]):
            color = 4    # Blue
        elif starts(line, "\""):
            color = 3    # Green
        return color
