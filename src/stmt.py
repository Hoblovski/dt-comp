"""
Statement generation.
"""
from .cgctx import *
from .expr import *

class Statement(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)

class ReturnStmt(Statement):
    def __init__(self, gs):
        super().__init__(gs)
        self.val = randexpr(gs)

    def emit(self, out):
        out.emitstr('return');
        self.val.emit(out)
        out.emitstr(';', newLine=True)

def randstmt(gs):
    return ReturnStmt(gs)
