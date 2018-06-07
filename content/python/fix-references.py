from pathlib import Path
import re


# 2018-06-07, A dirty script for refactoring reference links

def is_url(s):
    return s.startswith('http') or s.startswith('./') or s.startswith('/')  or s.startswith('../')



def walk(lines):
    begin = False
    start = True
    refs = []
    for l in lines:
        if re.match(r'^\*+ ', l):
            if refs:
                if not begin:
                    if prev != '\n':
                        yield '\n'
                    yield ':REFERENCES:\n'

                for r in refs:
                    yield r
                refs = []
                yield ':END:\n'
                yield '\n'
            yield l
            begin = False
            start = True
            prev = l
            continue

        if start or begin:
            if l.startswith('- ') and is_url(l[2:]):
                refs.append(l)
                continue
            else:
                start = False
                yield l
                prev = l
                continue

        if not begin and re.match(r'^(- )?-----', l):
            begin = True
            if prev != '\n':
                yield '\n'
            yield ':REFERENCES:\n'
            prev = l
            continue

        prev = l
        yield l

    if refs:
        if not begin:
            if prev != '\n':
                yield '\n'
            yield ':REFERENCES:\n'

        for r in refs:
            yield r
        refs = []
        yield ':END:\n'
        yield '\n'


def walk2(lines):
    start = False
    for l in lines:
        if re.match(r'^\*+ ', l):
            start = True
        else:
            if start and l == '\n':
                start = False
                continue
            else:
                start = False
        yield l


for p in Path('.').glob('**/README.org'):
    with open(p) as f:
        lines = [l for l in iter(f.readline, '')]

    lines = [l for l in walk(lines)]
    lines = [l for l in walk2(lines)]
    with open(p, 'w') as f:
        f.write(''.join(l for l in walk2(lines)).strip() + '\n')
