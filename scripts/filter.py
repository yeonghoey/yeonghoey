import os

from pandocfilters import Image, toJSONFilters


SRC = os.environ['YHY_FILTER_SRC']
BASE = os.environ['YHY_FILTER_BASE']

CONTEXT_PATH = os.path.dirname(SRC)


def fix_basepath(key, value, format, meta):
    if key == 'Image':
        value[2][0] = basepath(value[2][0])
        return Image(*value)


def basepath(url, raw=True):
    type_ = 'raw' if raw else 'tree'
    return '/'.join([BASE, type_, 'master', CONTEXT_PATH, url])


if __name__ == '__main__':
    toJSONFilters(filter(None, [
        fix_basepath if BASE else None
    ]))
