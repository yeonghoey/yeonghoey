from os import environ
from os.path import dirname
from pprint import pprint
from sys import stderr

import pandocfilters as pf


SRC = environ['YHY_FILTER_SRC']
BASE = environ['YHY_FILTER_BASE']
DEBUG = environ.get('YHY_FILTER_DEBUG') is not None

CONTEXT_PATH = dirname(SRC)


# When `handle_<function>` returns:
# pf.Foo : replace (spans as spans, divs as divs only)
#   None : do nohting
#     [] : delete

def handle_notag(key, value, format, meta):
    if key == 'Span':
        attr, inlines = value
        _, classes, _ = attr
        if 'tag' in classes:
            return []


def handle_basepath(key, value, format, meta):
    if key == 'Image':
        attr, inlines, target = value
        url, title = target
        return pf.Image(attr, inlines, (basepath(url), title))


def handle_debug(*args):
    print(file=stderr)
    names = 'key value format meta'.split()
    for n, a in zip(names, args):
        print(f'{n:6}: ', end='', file=stderr)
        pprint(a, indent=4, stream=stderr)
    print(file=stderr)


def basepath(url, raw=True):
    type_ = 'raw' if raw else 'tree'
    return '/'.join([BASE, type_, 'master', CONTEXT_PATH, url])


if __name__ == '__main__':
    pf.toJSONFilters(filter(None, [
        handle_debug if DEBUG else None,
        handle_notag,
        handle_basepath if BASE else None,
    ]))
