from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        keywords = ("if", "else", "finally", "try", "catch", "foreach",
                    "while", "continue", "pass", "break")
        if line.startswith(("include", "require")):
            color = color_map["blue"]
        elif line.startswith(("class", "public", "private", "function")):
            color = color_map["green"]
        elif line.startswith("def"):
            color = color_map["cyan"]
        elif line.startswith("return"):
            color = color_map["red"]
        elif line.startswith("$"):
            color = color_map["cyan"]
        elif line.startswith(("#", "//", "/*", "*/")):
            color = color_map["magenta"]
        elif line.startswith(keywords):
            color = color_map["yellow"]
        return color
