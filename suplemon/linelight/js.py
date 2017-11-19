from suplemon.linelight.color_map import color_map


class Syntax:
    def get_comment(self):
        return ("//", "")

    def get_color(self, raw_line):
        color = color_map["white"]
        line = raw_line.strip()
        if line.startswith("function"):
            color = color_map["cyan"]
        elif line.startswith("return"):
            color = color_map["red"]
        elif line.startswith("this."):
            color = color_map["cyan"]
        elif line.startswith(("//", "/*", "*/", "*")):
            color = color_map["magenta"]
        elif line.startswith(("if", "else", "for ", "while ", "continue", "break")):
            color = color_map["yellow"]
        return color
