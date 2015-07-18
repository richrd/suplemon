from helpers import *


class Syntax:
    def get_comment(self):
        return ("# ", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if starts(line, ["import", "from"]):
            color = 4    # Blue
        elif starts(line, "class"):
            color = 2    # Green
        elif starts(line, "def"):
            color = 6    # Cyan
        elif starts(line, ["return", "yield"]):
            color = 1    # Red
        elif starts(line, "self."):
            color = 6    # Cyan
        elif starts(line, ["#", "//", "\"", "'", ":"]):
            color = 5    # Magenta
        elif starts(line, ["if", "elif","else", "finally", "try", "except", "for ", "while ", "continue", "pass", "break"]):
            color = 3    # Yellow
        return color
