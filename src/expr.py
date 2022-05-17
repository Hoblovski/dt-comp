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
        out.emit('(', self.lhs, self.op, self.rhs, ')')

class UnaryExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.op = randlistitem(['-'])
        self.sub = randexpr(gs, depth)

    def emit(self, out):
        out.emit('(', self.op, self.sub, ')')

class VarRefExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.var = gs.randvar()

    def emit(self, out):
        out.emit('(', self.var, ')')

class AssignExpr(Expression):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.rhs = randexpr(gs, depth)
        # assignment can create new variables whose declaration will be hoisted to head of current block.
        if randn(100) <= 70 and len(gs.vars) > 0:
            self.lhs = gs.randvar()
        else:
            # must come after rhs to prevent uninited reads
            self.lhs = gs.freshvar()

    def emit(self, out):
        out.emit('(', self.lhs, '=', self.rhs, ')')

def randexpr(gs, depth):
    litw = 1
    binaryw = 2 if depth < Config.MaxExprDepth else 0
    unaryw = 1 if depth < Config.MaxExprDepth else 0
    assignw = 1 if depth < Config.MaxExprDepth else 0
    varw = 2 if depth < Config.MaxExprDepth else 0

    # ad hoc checks
    if len(gs.vars) == 0:
        varw = 0

    return randlistitemw([
        (litw, lambda: LitExpr(gs, depth+1)),
        (binaryw, lambda: BinaryExpr(gs, depth+1)),
        (unaryw, lambda: UnaryExpr(gs, depth+1)),
        (assignw, lambda: AssignExpr(gs, depth+1)),
        (varw, lambda: VarRefExpr(gs, depth+1)),
    ])()

