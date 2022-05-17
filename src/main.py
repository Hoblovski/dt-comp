"""Entry."""
import argparse
from .prog import *

def main():
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        '-s', '--seed', dest='seed', nargs='?', type=int,
        help='random generator seed')
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    gs = GeneratorState()
    prog = Program(gs)
    out = OutputManager()
    prog.emit(out)
