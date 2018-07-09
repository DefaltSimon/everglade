# coding=utf-8

from enum import Enum, auto

# TOKENS


class AutoName(Enum):
    """
    Helper class to generate better auto() values
    """
    def _generate_next_value_(self, start, count, last_values):
        return self


class TokenType(AutoName):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    LPAR = auto()
    RPAR = auto()

    EOF = auto()
    EOL = auto()

    ASSIGN = auto()
    DOLLAR = auto()
    TILDE = auto()
    COMMA = auto()
    ID = auto()

    # BEGIN = auto()
    # END = auto()

    SQ_BRACKET_L = auto()
    SQ_BRACKET_R = auto()
    C_BRACKET_L = auto()
    C_BRACKET_R = auto()


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()