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
        # current in-scope variables
        self.vars = []
        self.funcs = []

    def addFunc(self, f):
        self.funcs += [f]

    def randvar(self):
        return randlistitem(self.vars)
