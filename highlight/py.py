from helpers import *


class Syntax:
    def get_comment(self):
        return ("# ", "")

    def get_scope(self, raw_word):
        scope = "global"
        word = raw_word.strip()
        if starts(word, '"') and ends(word, '"'):
            scope = "string"
        elif word in ["class", "def"]:
            scope = "storage.type"
        elif starts(word, ["#", "//", "\"", "'"]):
            scope = "comment"
        elif word in ["if", "elif","else", "finally", "try", "except", "for ", "while ", "continue", "pass", "break", "import", "from", "return", "yield"]:
            scope = "keyword"
        elif word in ["+", "-", "*", "/", "+=", "-=", "/=", "*=", "=", "and", "or", "not", "<", ">", "!=", "is"]:
            scope = "keyword"
        elif word in ["True", "False", "None"]:
            scope = "constant.language"
        else:
            try:
                i = int(word)
                scope = "constant.numeric"
            except:
                try:
                    i = float(word)
                    scope = "constant.numeric"
                except:
                    pass

        return scope
