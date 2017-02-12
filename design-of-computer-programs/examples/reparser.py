from functools import update_wrapper
from pprint import pprint
import re


def grammar(description, whitespace=r'\s*'):
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def split(text, sep=None, maxsplit=-1):
    return [t.strip() for t in text.strip().split(sep, maxsplit)]


def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f


def parse(start_symbol, text, grammar):
    tokenizer = grammar[' '] + '(%s)'
    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)


REGRAMMER = grammar(r"""
RE      => REPEAT RE | REPEAT
REPEAT  => STAR | PLUS | SINGLE
STAR    => SINGLE [*]
PLUS    => SINGLE [+]
SINGLE  => DOT | LIT | ONEOF | ALT
DOT     => [.]
LIT     => \w+
ONEOF   => [[] \w+ []]
ALT     => [(] ALTLIST [)]
ALTLIST => RE [|] ALTLIST | RE
""")


def parse_re(pattern):
    tree, remains = parse('RE', pattern, REGRAMMER)
    if remains == '':
        return convert(tree)
    else:
        raise ValueError('Invalid Pattern: "%s", remains: %s'
                         % (pattern, remains))


def convert(tree):
    def walk(name, *args):
        if name in ('RE', 'REPEAT', 'SINGLE'):
            subtrees = [walk(*part) for part in args]
            return (subtrees[0] if len(subtrees) == 1 else
                    reduce(seq, subtrees))
        if name == 'DOT':
            return dot
        if name == 'LIT':
            return lit(args[0])
        if name == 'ONEOF':
            _, v, _ = args
            return oneof(v)
        if name == 'STAR':
            return star(walk(*args[0]))
        if name == 'PLUS':
            return plus(walk(*args[0]))
        if name == 'ALT':
            _, alist, _ = args
            return walk(*alist)
        if name == 'ALTLIST':
            if len(args) == 1:
                return walk(*args[0])
            else:
                a, _, remains = args
                return alt(walk(*a), walk(*remains))
    return walk(*tree)


def seq(a, b): return ('seq', a, b)
def lit(a):    return ('lit', a)
def oneof(s):  return ('oneof', s)
def star(a):   return ('star', a)
def plus(a):   return ('plus', a)
def alt(a, b): return ('alt', a, b)
dot = ('dot',)


def equals(actual, expected):
    if actual != expected:
        print '  actual: %s' % (actual,)
        print 'expected: %s' % (expected,)
        print '==> ' + ('pass' if actual == expected else 'fail') + '\n'


def test():
    equals(parse_re('.'), ('dot',))
    equals(parse_re('abc'), ('lit', 'abc'))
    equals(parse_re('[abc]'), ('oneof', 'abc'))
    equals(parse_re('a*'), ('star', ('lit', 'a')))
    equals(parse_re('a+'), ('plus', ('lit', 'a')))
    equals(parse_re('(a|b)'), ('alt', ('lit', 'a'), ('lit', 'b')))
    equals(parse_re('(a|b|c)'), ('alt',
                                 ('lit', 'a'),
                                 ('alt', ('lit', 'b'), ('lit', 'c'))))

    equals(parse_re('[ab]+'), ('plus', ('oneof', 'ab')))
    equals(parse_re('[ab]+c'), ('seq', ('plus', ('oneof', 'ab')), ('lit', 'c')))
    equals(parse_re('[ab]+c(d|e)'), ('seq',
                                     ('plus', ('oneof', 'ab')),
                                     ('seq', ('lit', 'c'),
                                      ('alt', ('lit', 'd'), ('lit', 'e')))))


test()
