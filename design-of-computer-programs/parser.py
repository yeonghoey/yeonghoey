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


def parse(start, g):
    pass


G = grammer('''
Expr   => Term [+-] Expr   | Term
Term   => Factor [*/] Term | Factor
Factor => Num              | [(] Expr [)]
Num    => [0-9]+
''')

pprint(G)
