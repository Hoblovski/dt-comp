"""
The generated function is unformatted. Probably use clang-format.
"""
import sys

from .randgen import *

class ProgNode:
    def __init__(self, gs):
        self.gs = gs

    def emit(self, out):
        pass


class Program(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)
        # we have only int type so needless to generate types
        self.funcs = [gs.randfunc()]

    def emit(self, out):
        for func in self.funcs[:-1]:
            func.emit(out)

        func = self.funcs[-1]
        func.name = 'main'
        func.emit(out)


class Function(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)
        self.name = f'f_{len(gs.funcs)}'
        # TODO: args
        self.body = gs.randstmt()
        gs.addFunc(self)

    def emit(self, out):
        out.emitstr('int')
        out.emitstr(self.name)
        out.emitstr('()')
        out.emitstr('{', newLine=True)
        self.body.emit(out)
        out.emitstr('}', newLine=True)

class Statement(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)

class ReturnStmt(Statement):
    def __init__(self, gs):
        super().__init__(gs)
        self.val = gs.randexpr()

    def emit(self, out):
        out.emitstr('return');
        self.val.emit(out)
        out.emitstr(';', newLine=True)

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
        self.lhs = gs.randexpr()
        self.rhs = gs.randexpr()

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
        self.sub = gs.randexpr()

    def emit(self, out):
        out.emitstr('(')
        out.emitstr(self.op)
        self.sub.emit(out)
        out.emitstr(')')

class OutputManager:
    def __init__(self):
        self.file = sys.stdout

    def emitstr(self, s, spBefore=' ', spAfter=' ', newLine=False):
        if newLine:
            spAfter = spAfter + '\n'
        self.file.write(spBefore + s + spAfter)

class GeneratorState:
    def __init__(self):
        # current in-scope variables
        self.vars = []
        self.funcs = []

    def addFunc(self, f):
        self.funcs += [f]

    def randvar(self):
        return randlistitem(self.vars)

    def randexpr(self):
        return randlistitem([
            lambda: LitExpr(self),
            lambda: BinaryExpr(self),
            lambda: UnaryExpr(self),
        ])()

    def randstmt(self):
        return ReturnStmt(self)

    def randfunc(self):
        return Function(self)

def main():
    gs = GeneratorState()
    prog = Program(gs)
    out = OutputManager()
    prog.emit(out)
