import helpers


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        keywords = ["if", "else", "finally", "try", "catch", "foreach",
                    "while", "continue", "pass", "break"]
        if helpers.starts(line, ["include", "require"]):
            color = 4    # Blue
        elif helpers.starts(line, ["class", "public", "private", "function"]):
            color = 2    # Green
        elif helpers.starts(line, "def"):
            color = 6    # Cyan
        elif helpers.starts(line, ["return"]):
            color = 1    # Red
        elif helpers.starts(line, "$"):
            color = 6    # Cyan
        elif helpers.starts(line, ["#", "//", "/*", "*/"]):
            color = 5    # Magenta
        elif helpers.starts(line, keywords):
            color = 3    # Yellow
        return color
