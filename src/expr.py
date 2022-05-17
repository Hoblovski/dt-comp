"""
Expression generation.
"""
from .cgctx import *
from .config import *

class Expression(ProgNode):
    def __init__(self, gs, depth):
        super().__init__(gs)
        self.depth = depth

class LitExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.val = randn(1000000)

    def emit(self, out):
        out.emitstr(str(self.val))

class BinaryExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.op = randlistitem(['+', '-', '*', '/', '%'])
        self.lhs = randexpr(gs, depth)
        self.rhs = randexpr(gs, depth)

    def emit(self, out):
        out.emitstr('(')
        self.lhs.emit(out)
        out.emitstr(self.op)
        self.rhs.emit(out)
        out.emitstr(')')

class UnaryExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.op = randlistitem(['-'])
        self.sub = randexpr(gs, depth)

    def emit(self, out):
        out.emitstr('(')
        out.emitstr(self.op)
        self.sub.emit(out)
        out.emitstr(')')

class VarRefExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.var = gs.randvar()

    def emit(self, out):
        out.emitstr('(')
        out.emitstr(self.var)
        out.emitstr(')')

class AssignExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.rhs = randexpr(gs, depth)
        # choose whether assign to existing variable or create a new one
        if randn(100) <= 70 and len(gs.vars) > 0:
            self.lhs = gs.randvar()
        else:
            # must come after rhs
            self.lhs = gs.freshvar()

    def emit(self, out):
        out.emitstr('(')
        out.emitstr(self.lhs)
        out.emitstr('=')
        self.rhs.emit(out)
        out.emitstr(')')

# handling lhs
# random generate variable: allow undefined variable (insert immediate variable)
def randexpr(gs, depth):
    binaryw = 0 if depth >= Config.MaxExprDepth else 1
    unaryw = 0 if depth >= Config.MaxExprDepth else 1
    assignw = 0 if depth >= Config.MaxExprDepth else 2
    varw = 0 if depth >= Config.MaxExprDepth else 2
    # fixme
    if len(gs.vars) == 0:
        varw = 0
    return randlistitemw([
        (1, lambda: LitExpr(gs, depth+1)),
        (binaryw, lambda: BinaryExpr(gs, depth+1)),
        (unaryw, lambda: UnaryExpr(gs, depth+1)),
        (assignw, lambda: AssignExpr(gs, depth+1)),
        (varw, lambda: VarRefExpr(gs, depth+1)),
    ])()

