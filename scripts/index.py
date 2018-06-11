from pathlib import Path
import re
from string import Template
import sys


with open('README.org') as f:
    main = f.read()

def to_link(src):
    return re.sub(r'^content/(.*)/README.org$', r'./\1', src)


def to_name(link):
    _, _, name = link.rpartition('/')
    return name


def to_indent(link):
    _, n = re.subn(r'/', r'', link)
    return '  ' * n


def to_elem(link):
    name = to_name(link)
    indent = to_indent(link)
    return f'{indent}- [[{link}][{name}]]'


srcs = (str(p) for p in Path('content').glob('**/README.org'))
links = sorted(to_link(s) for s in srcs)
elems = (to_elem(l) for l in links)
index = '\n'.join(elems)

with open('templates/index.org') as f:
    template = Template(f.read())

content = '\n'.join([main,
                     template.safe_substitute(index=index)])

TARGET = sys.argv[1]
with open(TARGET, 'w') as f:
    f.write(content)
