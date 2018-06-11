from collections import defaultdict
from pathlib import Path
from string import Template
import sys


def tree():
    return defaultdict(tree)


root = tree()

for src in Path('content').glob('**/README.org'):
    segments = src.parts[1:-1]
    node = root
    for s in segments:
        node = node[s]


def walk(node, parent='.', level=0):
    elems = sorted((k, v) for k, v in node.items())
    for name, subs in elems:
        indent = ' ' * level
        path = f'{parent}/{name}'
        link = f'[[{path}][{name}]]'
        yield f'{indent}- {link}'
        yield from walk(subs, path, level + 1)


with open('README.org') as f:
    head = f.read()

with open('templates/index.org') as f:
    template = Template(f.read())

index = '\n'.join(walk(root))
body = template.safe_substitute(index=index)


TARGET = sys.argv[1]
content = '\n'.join([head, body])
with open(TARGET, 'w') as f:
    f.write(content)
