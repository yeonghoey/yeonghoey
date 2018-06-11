from collections import defaultdict
from pathlib import Path
import re
from string import Template
import sys


def tree():
    return defaultdict(tree)


root = tree()

for src in Path('content').glob('**/README.org'):
    path = re.sub(r'^content/(.*)/README.org$', r'\1', str(src))
    segments = path.split('/')
    node = root
    for s in segments:
        node = node[s]
    node['__self__'] = path


def walk(node, level=0):
    elems = sorted((k, v) for k, v in node.items() if k != '__self__')
    for name, subs in elems:
        indent = ' ' * level
        path = subs.get('__self__')
        link = (f'[[./{path}][{name}]]' if path else
                f'{name}')
        yield f'{indent}- {link}'
        yield from walk(subs, level + 1)


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
