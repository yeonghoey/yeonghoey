from copy import deepcopy
import os

from pandocfilters import Image, toJSONFilters


SRC = os.environ['YHY_FILTER_SRC']
BASEURL = os.environ['YHY_FILTER_BASEURL']

SRCDIR = os.path.dirname(SRC)


def baseurl_fix(key, value, format, meta):
    if not BASEURL:
        return
    if key == 'Image':
        _, _, (url, _) = value
        new_ = deepcopy(value)
        new_[2][0] = '/'.join([BASEURL, SRCDIR, url])
        return Image(*new_)


if __name__ == '__main__':
    toJSONFilters([
        baseurl_fix,
    ])
