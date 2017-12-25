from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("# ", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        keywords = ("if", "elif", "else", "finally", "try", "except",
                    "for ", "while ", "continue", "pass", "break")
        if line.startswith(("import", "from")):
            color = color_map["blue"]
        elif line.startswith("class"):
            color = color_map["green"]
        elif line.startswith("def"):
            color = color_map["cyan"]
        elif line.startswith(("return", "yield")):
            color = color_map["red"]
        elif line.startswith("self."):
            color = color_map["cyan"]
        elif line.startswith(("#", "//", "\"", "'", ":")):
            color = color_map["magenta"]
        elif line.startswith(keywords):
            color = color_map["yellow"]
        return color
