"""Entry."""
from .prog import *

def main():
    gs = GeneratorState()
    prog = Program(gs)
    out = OutputManager()
    prog.emit(out)
