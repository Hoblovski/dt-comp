"""
Random generators.

TODO: combinators to fasten up
"""
import random

def randn(n):
    return random.randint(0, n-1)

def randbn(b, n):
    return random.randint(b, n-1)

def randlistitem(l):
    return l[randn(len(l))]

class AlphaBets:
    Lower = list("abcdefghijklmnopqrstuvwxyz")
    Upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    Digit = list("0123456789")
    AlphaNum = Lower + Upper + Digit

def randstr(l, prefix=''):
    res = ''.join([randlistitem(AlphaBets.AlphaNum) for _ in range(randbn(1, l))])
    return prefix + res

def randlistitemw(l):
    """Usage:
      weighted_choices( ('left', 1), ('right', 2), ('center', 2) )
      # 1/5 probability 'left', 2/5 'right', 2/5 'center'
      Supports zero weight.
    """
    prevsum = [w for (w, name) in l]
    for i in range(1, len(prevsum)):
        prevsum[i] += prevsum[i-1]
    pin = randn(prevsum[-1])
    for i, ps in enumerate(prevsum):
        if pin < ps:
            return l[i][1]
    raise Exception("unreachable")
