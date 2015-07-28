from suplemon import helpers


class Syntax:
    def get_comment(self):
        return ("# ", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        keywords = ["if", "elif", "else", "finally", "try", "except",
                    "for ", "while ", "continue", "pass", "break"]
        if helpers.starts(line, ["import", "from"]):
            color = 4    # Blue
        elif helpers.starts(line, "class"):
            color = 2    # Green
        elif helpers.starts(line, "def"):
            color = 6    # Cyan
        elif helpers.starts(line, ["return", "yield"]):
            color = 1    # Red
        elif helpers.starts(line, "self."):
            color = 6    # Cyan
        elif helpers.starts(line, ["#", "//", "\"", "'", ":"]):
            color = 5    # Magenta
        elif helpers.starts(line, keywords):
            color = 3    # Yellow
        return color
