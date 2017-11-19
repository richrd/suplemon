from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("/*", "*/")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if line.startswith("@import"):
            color = color_map["blue"]
        elif line.startswith("$"):
            color = color_map["green"]
        elif line.startswith("/*") or line.endswith("*/"):
            color = color_map["magenta"]
        elif line.startswith("{") or line.endswith(("}", "{")):
            color = color_map["cyan"]
        elif line.endswith(";"):
            color = color_map["yellow"]
        return color
