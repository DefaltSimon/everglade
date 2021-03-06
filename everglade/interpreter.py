# coding=utf-8
import logging
from typing import Union

from .ast_parser import Parser, ASTType
from .tokens import TokenType
from ._builtins import Builtins
from .state import ProgramState

log = logging.getLogger(__name__)


class NodeVisitor:
    def visit(self, node):
        name = "visit_" + type(node).__name__
        log.debug("Visting " + name)
        return getattr(self, name, self.generic)(node)

    def generic(self, node):
        raise TypeError("No visit method for {}".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser, state: ProgramState):
        self.parser = parser

        # INTERNAL STUFF
        self.state = state
        self.source_m = self.state.output

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

    def visit_Compound(self, node: ASTType):
        for c in node.children:
            self.visit(c)

    @staticmethod
    def visit_NoOp(node: ASTType):
        pass

    @staticmethod
    def visit_NoneType(_: ASTType):
        log.warning("Statement does not do anything.")

    def visit_Assign(self, node: ASTType):
        name = node.left.value
        self.state.global_scope[name] = self.visit(node.right)

    def visit_Var(self, node: ASTType):
        name = node.value
        value = self.state.global_scope.get(name)
        if value is None:
            raise UnboundLocalError("Variable is undefined: {}".format(name))
        else:
            return value

    def visit_Function(self, node: ASTType):
        # First check builtins
        fn = getattr(Builtins, node.fn.value)
        if not fn:
            # Try global scope
            fn = self.state.global_scope.get(node.fn.value)
            # TODO check if callable

        return fn(self.state, node.params)

    @staticmethod
    def visit_String(node: ASTType):
        return node.content

    def interpret(self):
        tree = self.parser.parse()
        # Parse from top down
        return self.visit(tree)
