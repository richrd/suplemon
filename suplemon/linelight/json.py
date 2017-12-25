from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self, line):
        return ("", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if line.startswith(("{", "}")):
            color = color_map["yellow"]
        elif line.startswith("\""):
            color = color_map["green"]
        return color
