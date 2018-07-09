# coding=utf-8
from everglade.tokens import TokenType, Token

ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz_"


def is_special(char: str) -> bool:
    return char in ALLOWED_CHARS


class Lexer:
    def __init__(self, raw_text):
        self.text = raw_text

        self.pos = 0
        self.char = self.text[self.pos]

    def shift(self):
        self.pos += 1

        # Check for end of text
        if self.pos > len(self.text) - 1:
            self.char = None
        else:
            self.char = self.text[self.pos]

    def peek(self, amount: int=1):
        peek_pos = self.pos + amount
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.char is not None and self.char.isspace():
            self.shift()

    def integer(self) -> int:
        res = ""
        while self.char is not None and self.char.isdigit():
            res += self.char
            self.shift()

        return int(res)

    def auto_number(self) -> Token:
        temp = str(self.integer())

        if self.char == ".":
            self.shift()
            temp += "." + str(self.integer())

            return Token(TokenType.FLOAT, float(temp))

        return Token(TokenType.INTEGER, int(temp))

    def string(self, char="\"") -> str:
        # Skip "
        self.shift()

        res = ""
        while self.char != char:
            res += self.char
            self.shift()

        # Skip second "/'
        self.shift()
        return res

    def reserved(self):
        """
        Handles reserved keywords
        """
        res = ""
        while self.char is not None and is_special(self.char):
            res += self.char
            self.shift()

        # tok = SPECIAL_KEYWORDS.get(res, Token(TokenType.ID, res))
        tok = Token(TokenType.ID, res)
        return tok

    def next_token(self):
        while self.char is not None:
            # Parses different tokens

            # VARIABLES, BASIC TYPES
            if self.char.isspace() and self.char != "\n":
                self.skip_whitespace()
                continue
            if self.char == "\n":
                self.shift()
                return Token(TokenType.EOL, "\n")

            # if self.char == "<" and self.peek() == "m":
            #     self.shift()
            #     self.shift()
            #     return Token(TokenType.BEGIN, "<m")
            # if self.char == "m" and self.peek() == ">":
            #     self.shift()
            #     self.shift()
            #     return Token(TokenType.END, "m>")

            if self.char.isdigit():
                # Could be FLOAT or INT
                return self.auto_number()
            # SPECIAL
            if is_special(self.char):
                return self.reserved()
            # STRING
            if self.char == "\"":
                return Token(TokenType.STRING, self.string())
            if self.char == "'":
                return Token(TokenType.STRING, self.string("'"))

            # OTHER OPERATORS
            if self.char == "=":
                self.shift()
                return Token(TokenType.ASSIGN, "=")
            if self.char == "$":
                self.shift()
                return Token(TokenType.DOLLAR, "$")
            if self.char == "~":
                self.shift()
                return Token(TokenType.TILDE, "~")
            if self.char == ",":
                self.shift()
                return Token(TokenType.COMMA, ",")

            if self.char == "[":
                self.shift()
                return Token(TokenType.SQ_BRACKET_L, "[")
            if self.char == "]":
                self.shift()
                return Token(TokenType.SQ_BRACKET_R, "[")

            if self.char == "{":
                self.shift()
                return Token(TokenType.C_BRACKET_L, "{")
            if self.char == "}":
                self.shift()
                return Token(TokenType.C_BRACKET_R, "}")

            # MATH
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
