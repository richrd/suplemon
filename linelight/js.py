from helpers import *

class Syntax:
    def get_comment(self):
        return ("//","")

    def get_color(self, raw_line):
        color = 0
        line = raw_line.strip()
        if starts(line, ["import", "from"]):
            color = 5    
        elif starts(line, "function"):
            color = 7    # Cyan
        elif starts(line, ["return"]):
            color = 2    # Red
        elif starts(line, "this."):
            color = 3    # Cyan
        elif starts(line, ["//", "/*", "*/", "*"]):
            color = 6    # Magenta
        elif starts(line, ["if", "else", "for ", "while ", "continue", "break"]):
            color = 4    # Yellow
        return color
