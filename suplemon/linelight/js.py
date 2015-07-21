import helpers


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if helpers.starts(line, ["import", "from"]):
            color = 4    # Blue
        elif helpers.starts(line, "function"):
            color = 6    # Cyan
        elif helpers.starts(line, ["return"]):
            color = 1    # Red
        elif helpers.starts(line, "this."):
            color = 6    # Cyan
        elif helpers.starts(line, ["//", "/*", "*/", "*"]):
            color = 5    # Magenta
        elif helpers.starts(line, ["if", "else", "for ", "while ", "continue", "break"]):
            color = 3    # Yellow
        return color
