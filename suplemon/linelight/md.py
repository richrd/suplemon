import helpers


class Syntax:
    def get_comment(self, line):
        return ("", "")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if helpers.starts(line, ["*", "-"]):  # List
            color = 6    # Cyan
        elif helpers.starts(line, "#"):  # Header
            color = 2    # Green
        elif helpers.starts(line, ">"):  # Item desription
            color = 3    # Yellow
        elif helpers.starts(raw_line, "    "):  # Code
            color = 5    # Magenta
        return color
