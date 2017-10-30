# coding=utf-8
from typing import Union

from .tokens import Token, TokenType
from .lexer import Lexer


class AST:
    pass

# AST operators


class BinOp(AST):
    """
    Binary operator: no precedence
    """
    def __init__(self, left: Token, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    """
    A number
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


ASTType = Union[BinOp, Num]


# PARSER

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        # Gets first token
        self.current = self.lexer.next_token()

    def move(self, token_type: TokenType):
        if self.current.type == token_type:
            self.current = self.lexer.next_token()
        else:
            raise TypeError("unexpected token, wanted {}".format(token_type))


    # GRAMMAR
    def factor(self):
        """
        INT | LPAR expr RPAR
        """
        token = self.current
        if token.type == TokenType.INTEGER:
            self.move(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAR:
            self.move(TokenType.LPAR)
            node = self.expr()
            self.move(TokenType.RPAR)
            return node

    def term(self):
        """
        factor ((MUL | DIV) factor)*
        """
        node = self.factor()

        while self.current.type in (TokenType.MUL, TokenType.DIV):
            token = self.current

            if token.type == TokenType.MUL:
                self.move(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.move(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current

            if token.type == TokenType.PLUS:
                self.move(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.move(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        """
        Parse whole expression
        """
        return self.expr()
