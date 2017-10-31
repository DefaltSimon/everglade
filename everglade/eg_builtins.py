# coding=utf-8


class Builtins:
    @staticmethod
    def raw(ctx, *param):
        print("got", param)