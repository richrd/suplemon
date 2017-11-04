from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("<!--", "-->")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if line.startswith(("#", "//", "/*", "*/", "<!--")):
            color = color_map["magenta"]
        elif line.endswith(("*/", "-->")):
            color = color_map["magenta"]
        elif line.startswith("<"):
            color = color_map["cyan"]
        elif line.endswith(">"):
            color = color_map["cyan"]
        return color
