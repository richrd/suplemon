from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self, line):
        return ("", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if line.startswith(("*", "-")):  # List
            color = color_map["cyan"]
        elif line.startswith("#"):  # Header
            color = color_map["green"]
        elif line.startswith(">"):  # Item description
            color = color_map["yellow"]
        elif raw_line.startswith("    "):  # Code
            color = color_map["magenta"]
        return color
