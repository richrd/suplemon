from helpers import *

class Syntax:
    def get_comment(self):
        return ("//","")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if starts(line, ["import", "from"]):
            color = 4    # Blue
        elif starts(line, "function"):
            color = 6    # Cyan
        elif starts(line, ["return"]):
            color = 1    # Red
        elif starts(line, "this."):
            color = 6    # Cyan
        elif starts(line, ["//", "/*", "*/", "*"]):
            color = 5    # Magenta
        elif starts(line, ["if", "else", "for ", "while ", "continue", "break"]):
            color = 3    # Yellow
        return color
