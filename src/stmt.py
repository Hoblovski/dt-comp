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
        out.emit('return', self.val, ';', br=True)

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
        out.emit('{', br=True)
        for hdecl in self.hdecls:
            out.emit('int', hdecl, ';', br=True)
        out.emit(*self.subs)
        out.emit('}', br=True)

class IfStmt(Statement):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)

        self.cond = randexpr(gs, 0)
        self.thclause = randstmt(gs, depth)
        if randn(100) < 60:
            self.elclause = randstmt(gs, depth)
        else:
            self.elclause = None

    def emit(self, out):
        out.emit('if', '(', self.cond, ')', br=True)
        out.emit(self.thclause)
        if self.elclause is not None:
            out.emit('else', self.elclause, br=True)

class ExprStmt(Statement):
    def __init__(self, gs, depth):
        super().__init__(gs, depth)
        # generate assignments at higher probability
        if randn(100) <= 80:
            self.expr = AssignExpr(gs, 0)
        else:
            self.expr = randexpr(gs, 0)

    def emit(self, out):
        out.emit(self.expr, ';', br=True)

def randstmt(gs, depth, noBlock=False):
    exprw = 10
    returnw = 1
    blockw = 3 if depth < Config.MaxBlockDepth else 0
    ifw = 3 if depth < Config.MaxBlockDepth else 0

    rv= randlistitemw([
        (exprw, lambda: ExprStmt(gs, depth+1)),
        (returnw, lambda: ReturnStmt(gs, depth+1)),
        (blockw, lambda: BlockStmt(gs, depth+1)),
        (ifw, lambda: IfStmt(gs, depth+1)),
    ])()
    return rv
