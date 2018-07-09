# coding=utf-8
from typing import Union

from .tokens import Token, TokenType
from .lexer import Lexer


class AST:
    pass

# AST operators


class BinOp(AST):
    """
    Binary operator
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


class String(AST):
    def __init__(self, content):
        self.content = content


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Function(AST):
    def __init__(self, fn, params):
        self.fn = fn
        self.params = params


class NoOp(AST):
    pass


ASTType = Union[BinOp, Num, Var, Assign, Compound, NoOp, Function, String]


# PARSER

class Parser:
    def __init__(self, lexer: Union[Lexer, str]):
        if not isinstance(lexer, Lexer):
            self.lexer = Lexer(lexer)
        else:
            self.lexer = lexer

        # Gets first token
        self.current = self.lexer.next_token()

    def move(self, token_type: TokenType):
        if self.current.type == token_type:
            self.current = self.lexer.next_token()
        else:
            raise TypeError("unexpected token {}, wanted {}".format(self.current, token_type))

    # GRAMMAR
    def factor(self):
        """
        factor: PLUS factor
              | MINUS factor
              | INT
              | FLOAT
              | STRING
              | LPAR expr RPAR
              | variable
        """
        token = self.current

        if token.type == TokenType.PLUS:
            self.move(TokenType.PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.MINUS:
            self.move(TokenType.MINUS)
            return UnaryOp(token, self.factor())

        if token.type == TokenType.INTEGER:
            self.move(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.FLOAT:
            self.move(TokenType.FLOAT)
            return token

        elif token.type == TokenType.LPAR:
            self.move(TokenType.LPAR)
            node = self.expr()
            self.move(TokenType.RPAR)
            return node

        elif token.type == TokenType.STRING:
            self.move(TokenType.STRING)
            return String(token.value)

        else:
            node = self.variable()
            return node

    def term(self):
        """
        term: factor ((MUL | DIV) factor)*
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
        expr: term ((PLUS | MINUS) term)*
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

    # Second part
    def program(self):
        """
        program: statement_list EOF
        """
        root = Compound()

        nodes = self.statement_list()

        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self, end_type=TokenType.EOL) -> list:
        """
        statement_list: (statement EOL)*
        """
        stmt = self.statement()

        res = [stmt]
        while self.current.type == end_type:
            self.move(TokenType.EOL)
            res.append(self.statement())

        return res

    def statement(self):
        """
        statement: assignment_statement | execution_statement
                 | def_statement | empty | comment
        """
        # Assignment
        if self.current.type == TokenType.ID:
            return self.assignment_stmt()
        # Function execution
        if self.current.type == TokenType.DOLLAR:
            return self.execution_stmt()

        # TODO

    def assignment_stmt(self):
        """
        assignment_statement: variable ASSIGN expr
        """
        var = self.variable()
        # Must be ASSIGN
        assign = self.current
        self.move(TokenType.ASSIGN)
        value = self.expr()

        return Assign(var, assign, value)

    def parameter_list(self):
        first = self.expr()

        nodes = [first]
        while self.current.type == TokenType.COMMA:
            self.move(TokenType.COMMA)
            nodes.append(self.expr())

        return nodes

    def execution_stmt(self):
        self.move(TokenType.DOLLAR)

        fn_name = self.variable()

        # Has parameters
        if self.current.type == TokenType.LPAR:
            self.move(TokenType.LPAR)
            param = self.parameter_list()
            self.move(TokenType.RPAR)
        else:
            param = []

        return Function(fn_name, param)

    def variable(self):
        node = Var(self.current)
        self.move(TokenType.ID)
        return node

    @staticmethod
    def empty():
        return NoOp()

    # STARTING METHOD
    def parse(self):
        node = self.program()
        return node
