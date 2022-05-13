"""
Function/top-level generation.
"""
from .randgen import *
from .stmt import *

class Program(ProgNode):
    def __init__(self, gs):
        super().__init__(gs)
        # we have only int type so needless to generate types
        self.funcs = [Function(gs)]

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
        self.body = randstmt(gs)
        gs.addFunc(self)

    def emit(self, out):
        out.emitstr('int')
        out.emitstr(self.name)
        out.emitstr('()')
        out.emitstr('{', newLine=True)
        self.body.emit(out)
        out.emitstr('}', newLine=True)

