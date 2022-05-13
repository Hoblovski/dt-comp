"""
Expression generation.
"""
from .cgctx import *

class Expression(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)

class LitExpr(Expression):
    def __init__(self, gs):
        super().__init__(gs)
        self.val = randn(1000000)

    def emit(self, out):
        out.emitstr(str(self.val))

class BinaryExpr(Expression):
    def __init__(self, gs):
        super().__init__(gs)
        self.op = randlistitem(['+', '-', '*', '/', '%'])
        self.lhs = randexpr(gs)
        self.rhs = randexpr(gs)

    def emit(self, out):
        out.emitstr('(')
        self.lhs.emit(out)
        out.emitstr(self.op)
        self.rhs.emit(out)
        out.emitstr(')')

class UnaryExpr(Expression):
    def __init__(self, gs):
        super().__init__(gs)
        self.op = randlistitem(['-'])
        self.sub = randexpr(gs)

    def emit(self, out):
        out.emitstr('(')
        out.emitstr(self.op)
        self.sub.emit(out)
        out.emitstr(')')

def randexpr(gs):
    return randlistitem([
        lambda: LitExpr(gs),
        lambda: BinaryExpr(gs),
        lambda: UnaryExpr(gs),
    ])()
