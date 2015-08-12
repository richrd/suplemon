from suplemon import helpers


class Syntax:
    def get_comment(self):
        return ("<!--", "-->")

    def get_color(self, raw_line):
        color = 7
        line = raw_line.strip()
        if helpers.starts(line, ["#", "//", "/*", "*/", "<!--"]):
            color = 5    # Magenta
        elif helpers.ends(line, ["*/", "-->"]):
            color = 5    # Magenta
        elif helpers.starts(line, "<"):
            color = 6    # Cyan
        elif helpers.ends(line, ">"):
            color = 6    # Cyan
        return color
