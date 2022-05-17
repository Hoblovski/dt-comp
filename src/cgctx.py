"""
Code generation contexts.
"""
from .randgen import *
import sys

class ProgNode:
    """Base type for program constructs."""
    def __init__(self, gs):
        self.gs = gs

    def emit(self, out):
        pass

class OutputManager:
    """Naive unformatted output."""
    def __init__(self):
        self.file = sys.stdout

    def emitstr(self, s, spBefore=' ', spAfter=' ', newLine=False):
        if newLine:
            spAfter = spAfter + '\n'
        self.file.write(spBefore + s + spAfter)

class GeneratorState:
    """Static state of the generating program. Used to aid generation."""
    def __init__(self):
        self.funcs = []
        # current in-scope variables
        self.vars = []

        self._curblks = []
        # used for enterblk & exitblk
        self._ovlen = []

    def addFunc(self, f):
        self.funcs += [f]

    def randvar(self):
        return randlistitem(self.vars)

    def freshvar(self):
        name = None
        while True:
            name = randstr(l=3, prefix='l_')
            if all(x != name for x in self.vars):
                break
        self._curblks[-1].hoistdecl(name)
        self.vars += [name]
        return name

    def enterblk(self, blk):
        self._ovlen += [len(self.vars)]
        self._curblks += [blk]

    def exitblk(self):
        self._curblks.pop()
        t = self._ovlen.pop()
        self.vars = self.vars[:t]
