# coding=utf-8

"""
Manages interpreter output and state
"""


class Output:
    def __init__(self):
        self.parts = []

    def add(self, *sources: str, end="\n"):
        # Don't add lines with only spaces
        for s in sources:
            self.parts.append(str(s))
            self.parts.append(end)

    def __str__(self) -> str:
        return "".join(self.parts)

    def get_output(self) -> str:
        return self.__str__()


class ProgramState:
    def __init__(self, output: Output):
        self.global_scope = {}
        self.output = output
