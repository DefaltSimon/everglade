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
    STRING = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    LPAR = auto()
    RPAR = auto()

    EOF = auto()


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