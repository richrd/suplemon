import helpers


class Syntax:
    def get_comment(self):
        return ("/*", "*/")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if helpers.starts(line, "@import"):
            color = 4    # Blue
        elif helpers.starts(line, "$"):
            color = 2    # Green
        elif helpers.starts(line, "/*") or helpers.ends(line, "*/"):
            color = 5    # Magenta
        elif helpers.starts(line, "{") or helpers.ends(line, "}") or helpers.ends(line, "{"):
            color = 6    # Cyan
        elif helpers.ends(line, ";"):
            color = 3    # Yellow
        return color
