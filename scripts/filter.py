from os import environ
from os.path import dirname
from pprint import pprint
from sys import stderr

from pandocfilters import Image, toJSONFilters


SRC = environ['YHY_FILTER_SRC']
BASE = environ['YHY_FILTER_BASE']
DEBUG = environ.get('YHY_FILTER_DEBUG') is not None

CONTEXT_PATH = dirname(SRC)


def handle_basepath(key, value, format, meta):
    if key == 'Image':
        value[2][0] = basepath(value[2][0])
        return Image(*value)


def handle_debug(*arg):
    pprint(arg, stream=stderr)


def basepath(url, raw=True):
    type_ = 'raw' if raw else 'tree'
    return '/'.join([BASE, type_, 'master', CONTEXT_PATH, url])


if __name__ == '__main__':
    toJSONFilters(filter(None, [
        handle_basepath if BASE else None,
        handle_debug if DEBUG else None,
    ]))
