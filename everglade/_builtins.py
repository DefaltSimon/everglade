# coding=utf-8
from typing import Tuple
from .ast_parser import ASTType, Var, String, Num


def get_token_value(token):
    if isinstance(token, Var):
        return token.value
    elif isinstance(token, String):
        return token.content
    elif isinstance(token, Num):
        return token.value


class Builtins:
    @staticmethod
    def out(state, params: Tuple[ASTType]):
        for p in params:
            res = get_token_value(p)
            if res:
                state.output.add(res)

    @staticmethod
    def escape_json(state, text):
        print("state", state)
        print("text", text)