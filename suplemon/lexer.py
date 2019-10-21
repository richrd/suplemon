# -*- encoding: utf-8

import logging
import pygments
import pygments.token
import pygments.lexers


class Lexer:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.token_map = {
            pygments.token.Text:                       "generic",
            pygments.token.Generic.Strong:             "string",
            pygments.token.Generic.Subheading:         "string",
            pygments.token.Generic.Deleted:            "invalid",
            pygments.token.Punctuation:                "punctuation",
            pygments.token.Operator:                   "keyword",
            pygments.token.Operator.Word:              "keyword.control",

            pygments.token.Comment:                    "comment",
            pygments.token.Comment.Single:             "comment",
            pygments.token.Comment.Multiline:          "comment",

            pygments.token.Name:                       "entity.name",
            pygments.token.Name.Other:                 "entity.name",
            pygments.token.Name.Tag:                   "entity.name.tag",
            pygments.token.Name.Class:                 "entity.name.class",
            pygments.token.Name.Function:              "entity.name.function",
            pygments.token.Name.Function.Magic:        "entity.name.function",
            pygments.token.Name.Attribute:             "entity.other.attribute-name",
            pygments.token.Name.Variable:              "variable",
            pygments.token.Name.Variable.Magic:        "variable",
            pygments.token.Name.Builtin:               "constant.language",
            pygments.token.Name.Builtin.Pseudo:        "constant.language",
            pygments.token.Name.Namespace:             "constant.language",

            pygments.token.Literal.String:             "string",
            pygments.token.Literal.String.Doc:         "string",
            pygments.token.Literal.String.Double:      "string",
            pygments.token.Literal.String.Regex:       "string",
            pygments.token.Literal.String.Backtick:    "string",
            pygments.token.Literal.String.Interpol:    "string.interpolated",
            pygments.token.Literal.Number:             "constant.numeric",
            pygments.token.Literal.Number.Hex:         "constant.numeric",
            pygments.token.Literal.Number.Float:       "constant.numeric",
            pygments.token.Literal.Number.Integer:     "constant.numeric",

            pygments.token.Keyword:                    "keyword",
            pygments.token.Keyword.Reserved:           "constant.language",
            pygments.token.Keyword.Constant:           "constant.language",
            pygments.token.Keyword.Namespace:          "keyword",
            pygments.token.Keyword.Declaration:        "keyword",

            pygments.token.Error:                      "invalid",
        }

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

            if token in self.token_map.keys():
                scope = self.token_map[token]
            else:
                self.logger.warning("Token '{0}' for word '{1}' not found in token_map.".format(token, word[1]))

            scopes.append((scope, word[1]))
        return scopes
