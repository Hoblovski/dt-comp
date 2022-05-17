"""Entry."""
import argparse
from .prog import *
import sys

def main():
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        '-s', '--seed', dest='seed', nargs='?', type=int,
        help='random generator seed')
    args = parser.parse_args()

    if args.seed is not None:
        seed = args.seed
    else:
        seed = randn(sys.maxsize)

    random.seed(seed)
    gs = GeneratorState()
    prog = Program(gs)
    out = OutputManager()
    out.emit(f'/* seed = {seed} */\n', br=True)
    prog.emit(out)
