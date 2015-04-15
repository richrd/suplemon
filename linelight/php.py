from helpers import *

class Syntax:
    def get_comment(self):
        return ("//","")

    def get_color(self, raw_line):
        color = 0
        line = raw_line.strip()
        if starts(line, ["include", "require"]):
            color = 5
        elif starts(line, ["class","public" ,"private" ,"function"]):
            color = 3    # Green
        elif starts(line, "def"):
            color = 7    # Cyan
        elif starts(line, ["return"]):
            color = 2    # Red
        elif starts(line, "$"):
            color = 7    # Cyan
        elif starts(line, ["#", "//", "/*", "*/"]):
            color = 6    # Magenta
        elif starts(line, ["if", "else", "finally", "try", "catch", "foreach", "while", "continue", "pass", "break"]):
            color = 4    # Yellow
        return color
