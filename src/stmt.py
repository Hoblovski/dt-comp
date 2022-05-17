"""
Statement generation.
"""
from .cgctx import *
from .expr import *
from .config import *

class Statement(ProgNode):
    def __init__(self, gs, depth):
        super().__init__(gs)
        self.depth = depth

class ReturnStmt(Statement):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        self.val = randexpr(gs, 0)

    def emit(self, out):
        out.emitstr('return');
        self.val.emit(out)
        out.emitstr(';', newLine=True)

class BlockStmt(Statement):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)

        self.hdecls = []
        gs.enterblk(self)
        self.subs = [randstmt(gs, depth) for _ in range(randn(Config.MaxBlockStmt))]
        gs.exitblk()

    def hoistdecl(self, name):
        assert isinstance(name, str)
        self.hdecls += [name]

    def emit(self, out):
        out.emitstr('{', newLine=True);
        for hdecl in self.hdecls:
            out.emitstr('int')
            out.emitstr(hdecl)
            out.emitstr(';', newLine=True)
        for sub in self.subs:
            sub.emit(out)
        out.emitstr('}', newLine=True)

class ExprStmt(Statement):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        # generate assignments at higher probability
        if randn(100) <= 80:
            self.expr = AssignExpr(gs, 0)
        else:
            self.expr = randexpr(gs, 0)

    def emit(self, out):
        self.expr.emit(out)
        out.emitstr(';', newLine=True)

def randstmt(gs, depth, noBlock=False):
    blockWeightDefault = 2
    blockWeight = 0 if depth >= Config.MaxBlockDepth else blockWeightDefault

    rv= randlistitemw([
        (10, lambda: ExprStmt(gs, depth+1)),
        (1, lambda: ReturnStmt(gs, depth+1)),
        (blockWeight, lambda: BlockStmt(gs, depth+1)),
    ])()
    return rv
