# coding=utf-8
from .tokens import TokenType, Token


class Lexer:
    def __init__(self, raw_text):
        self.text = raw_text

        self.pos = 0
        self.char = self.text[self.pos]

    def shift(self):
        self.pos += 1

        # Check for end of text
        if self.pos > len(self.text) -1:
            self.char = None
        else:
            self.char = self.text[self.pos]

    def skip_whitespace(self):
        while self.char is not None and self.char.isspace():
            self.shift()

    def integer(self):
        res = ""
        while self.char is not None and self.char.isdigit():
            res += self.char
            self.shift()

        return int(res)

    def next_token(self):
        while self.char is not None:

            # Parses different tokens
            if self.char.isspace():
                self.skip_whitespace()
                continue

            if self.char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.char == "+":
                self.shift()
                return Token(TokenType.PLUS, "+")
            if self.char == "-":
                self.shift()
                return Token(TokenType.MINUS, "-")

            if self.char == "*":
                self.shift()
                return Token(TokenType.MUL, "*")
            if self.char == "/":
                self.shift()
                return Token(TokenType.DIV, "/")

            if self.char == "(":
                self.shift()
                return Token(TokenType.LPAR, "(")
            if self.char == ")":
                self.shift()
                return Token(TokenType.RPAR, ")")

            # Not a valid token
            raise TypeError("not a valid token: {}".format(self.char))

        return Token(TokenType.EOF, None)

