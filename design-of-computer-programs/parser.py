# -*- coding: utf-8 -*-
from pprint import pprint
import re


def grammer(description):
    g = {}
    for line in split(description, '\n'):
        atom, expansion = split(line, ' => ')
        alternatives = split(expansion, ' \| ')
        g[atom] = tuple(split(seq, ' ') for seq in alternatives)
    return g


def split(s, pattern):
    return [p.strip() for p in re.split(pattern, s.strip())]


def parse(start, text, g):
    def parse_atom(pattern, text):
        pattern = r'^\s*' + '(%s)' % pattern
        mo = re.match(pattern, text)
        return ((mo.group(1), text[mo.end():]) if mo is not None else Fail)

    def parse_sequence(sequence, text):
        tree, remains = [], text
        for target in sequence:
            if target in g:
                subtrees, r = go(target, remains)
                if subtrees is None:
                    return Fail
                else:
                    tree.append(subtrees)
                    remains = r
            else:
                parsed, r = parse_atom(target, remains)
                if parsed is None:
                    return Fail
                else:
                    tree.append(parsed)
                    remains = r

        return (tree, remains)

    def go(target, text):
        sequences = g[target]
        for seq in sequences:
            subtrees, remains = parse_sequence(seq, text)
            if subtrees is not None:
                return ([target] + subtrees, remains)
        return Fail

    return go(start, text)


G = grammer('''
Expr   => Term [+-] Expr   | Term
Term   => Factor [*/] Term | Factor
Factor => Num              | [(] Expr [)]
Num    => [0-9]+
''')

Fail = (None, None)

pprint(G)
pprint(parse('Expr', '4 * (1 + 2) * 3', G))
