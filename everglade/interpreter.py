# coding=utf-8
from typing import Union

from .ast_parser import Parser, ASTType
from .tokens import TokenType

# TODO add interpreter


class NodeVisitor:
    def visit(self, node):
        name = "visit_" + type(node).__name__
        return getattr(self, name, self.generic)(node)

    def generic(self, node):
        raise TypeError("No visit method for {}".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_BinOp(self, node: ASTType) -> Union[int, float]:
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    @staticmethod
    def visit_Num(node: ASTType) -> Union[int, float]:
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        # Parse from top down
        return self.visit(tree)
