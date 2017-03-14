# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
import os
import re
import sys


def main(base):
    elems = []
    for name in os.listdir(base):
        if name == 'README.org':
            continue
        p = os.path.join(base, name)
        if name.endswith('.org') and os.path.isfile(p):
            title = read_title(p)
            if title is None:
                print('Failed to parse: %s' % p, file=sys.stderr)
            else:
                elems.append((title, name))

    print('* %s' % base.capitalize())
    dump(elems)


def read_title(path):
    with open(path) as f:
        line = next(f)
        m = re.match(r'^\* (.*)$', line)
        if m is not None:
            return m.group(1).strip()
        m = re.match(r'^#\+TITLE\s*:(.*)$', line)
        if m is not None:
            return m.group(1).strip()
        else:
            return None


def dump(elems):
    for title, name in sorted(elems):
        print('- [[%s][%s]]' % (name, title))


if __name__ == '__main__':
    main(sys.argv[1])
