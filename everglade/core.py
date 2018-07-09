# coding=utf-8
import re
import logging
from typing import Union, TextIO

# REVERT
from everglade.ast_parser import Parser
from everglade.interpreter import Interpreter
from everglade.state import ProgramState, Output

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

RE_CAP = re.compile(r"<m\n[\s\S]+?\nm>", flags=re.DOTALL | re.MULTILINE)


# TEST function
def process_text(text: str, regex=RE_CAP):
    splits = []

    # keeps track of the last chunk
    last_pos = 0

    iterator = regex.finditer(text)
    for chunk in iterator:
        start = chunk.start()
        end = chunk.end()

        # Match doesn't start at the beginning
        if start != 0:
            # This indicates part of .eg code that is not inside <m m>
            # Collapse spaces and stuff
            code = text[last_pos:start].strip(" ")
            # Do not add if these are empty lines / spaces
            if code:
                # Add to list and indicate that this is "native" minecraft stuff, not to be parsed
                splits.append({"raw": code, "parse": False})

                # Update last position track
                last_pos = end

        # Add also the everglade code inside <m m>
        eg_code = text[start:end]

        # Clean up the code (remove <m, m>, \n, ...)
        eg_code = eg_code.lstrip("<m").rstrip("m>").strip("\n")

        # Add to list and set to be parsed
        splits.append({"raw": eg_code, "parse": True})

        # In case the above if statement didn't execute, update last_pos
        last_pos = end

    return splits


class Everglade:
    def __init__(self, inp: Union[str, TextIO]):
        # Check if inp is file-like
        if hasattr(inp, "read"):
            # Assume this is TextIO or similar
            self.raw = inp.read()
        else:
            self.raw = str(inp)

        self.processed = process_text(self.raw)
        log.debug("Processed: " + str(self.processed))

    @staticmethod
    def _make_interp(raw, state):
        parser = Parser(raw)
        interp = Interpreter(parser, state)

        return interp

    def compile_eg(self):
        out = Output()
        state = ProgramState(out)

        for chunk in self.processed:
            # Parse chunks marked
            if chunk["parse"] is True:
                log.info("Parsing new chunk")
                log.debug(chunk["raw"])
                interp = self._make_interp(chunk["raw"], state)
                # Automatically adds "compiled" code to "out"
                interp.interpret()
            else:
                out.add(chunk["raw"])

        return out.get_output().strip("\n")
