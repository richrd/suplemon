from helpers import *

class Syntax:
    def get_comment(self):
        return ("//","")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if starts(line, ["include", "require"]):
            color = 4    # Blue
        elif starts(line, ["class","public" ,"private" ,"function"]):
            color = 2    # Green
        elif starts(line, "def"):
            color = 6    # Cyan
        elif starts(line, ["return"]):
            color = 1    # Red
        elif starts(line, "$"):
            color = 6    # Cyan
        elif starts(line, ["#", "//", "/*", "*/"]):
            color = 5    # Magenta
        elif starts(line, ["if", "else", "finally", "try", "catch", "foreach", "while", "continue", "pass", "break"]):
            color = 3    # Yellow
        return color
