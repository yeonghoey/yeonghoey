from copy import deepcopy
import os
from urllib.parse import urljoin

from pandocfilters import Image, toJSONFilters


SRC = os.environ['YHY_SRC']
BASEURL = os.environ['YHY_BASEURL']

SRCDIR = os.path.dirname(SRC)


def baseurl_fix(key, value, format, meta):
    if not BASEURL:
        return
    if key == 'Image':
        _, _, (url, _) = value
        new_ = deepcopy(value)
        new_[2][0] = urljoin(BASEURL, '/'.join([SRCDIR, url]))
        return Image(*new_)


if __name__ == '__main__':
    toJSONFilters([
        baseurl_fix,
    ])
