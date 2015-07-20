# -*- encoding: utf-8

import pygments
import pygments.lexers


class Lexer:
    def __init__(self, app):
        self.app = app

    def lex(self, code, lex):
        """Return tokenified code.

        Return a list of tuples (scope, word) where word is the word to be
        printed and scope the scope name representing the context.

        :param str code: Code to tokenify.
        :param lex: Lexer to use.
        :return:
        """
        if lex is None:
            if not type(code) is str:
                # if not suitable lexer is found, return decoded code
                code = code.decode("utf-8")
            return (("global", code),)

        words = pygments.lex(code, lex)

        scopes = []
        for word in words:
            token = word[0]
            scope = "global"

            if token in pygments.token.Keyword:
                scope = "keyword"
            elif token == pygments.token.Comment:
                scope = "comment"
            elif token in pygments.token.Literal.String:
                scope = "string"
            elif token in pygments.token.Literal.Number:
                scope = "constant.numeric"
            elif token == pygments.token.Name.Function:
                scope = "entity.name.function"
            elif token == pygments.token.Name.Class:
                scope = "entity.name.class"
            elif token == pygments.token.Name.Tag:
                scope = "entity.name.tag"
            elif token == pygments.token.Operator:
                scope = "keyword"
            elif token == pygments.token.Name.Builtin.Pseudo:
                scope = "constant.language"

            scopes.append((scope, word[1]))
        return scopes
