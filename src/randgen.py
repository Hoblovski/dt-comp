# combinators
import random

def randn(n):
    return random.randint(0, n-1)

class RandGen:
    """
    Random generator combinators
    """
    class AlphaBets:
        Lower = list("abcdefghijklmnopqrstuvwxyz")
        Upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        Digit = list("0123456789")

    def randintgen(v1, v2=None):
        if v2 is None:
            v1, v2 = 0, v1
        def f():
            return random.randint(v1, v2-1)
        return f

    def randstrgen(maxlen, alphabet=None, quote=None):
        alphabet = alphabet or RandGen.AlphaBets.Lower
        def f():
            res = ''.join([alphabet[random.randint(0, len(alphabet)-1)] for _ in range(random.randint(1, maxlen))])
            if quote is not None:
                res = quote + res + quote
            return res
        return f

    def either(left, right, leftprob=0.5):
        def f():
            if random.random() < leftprob:
                return left()
            else:
                return right()
        return f

    def choose(*choices):
        def f():
            return choices[random.randint(0, len(choices)-1)]
        return f

    def weighted_choose(*weighted_choices):
        """Usage:
          weighted_choices( ('left', 1), ('right', 2), ('center', 2) )
          # 1/5 probability 'left', 2/5 'right', 2/5 'center'
        """
        prevsum = [weight for (name, weight) in weighted_choices]
        for i in range(1, len(prevsum)):
            prevsum[i] += prevsum[i-1]
        def f():
            t = random.randint(0, prevsum[-1]-1)
            for i in range(len(prevsum)):
                if t < prevsum[i]:
                    return weighted_choices[i][0]
        return f

def randstr(l, prefix=''):
    return prefix + RandGen.randstrgen(l)

def randlistitem(l):
    return l[randn(len(l))]
