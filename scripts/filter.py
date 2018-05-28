from copy import deepcopy
import os
from urllib.parse import urljoin

from pandocfilters import Image, toJSONFilters


SRC = os.environ['YHY_FILTER_SRC']
SRCDIR = os.path.dirname(SRC)
BASEURL = os.environ['YHY_FILTER_BASEURL']


def baseurl_fix(key, value, format, meta):
    if key == 'Image':
        url = value[2][0]
        value[2][0] = urljoin(BASEURL, os.path.join(SRCDIR, url))
        return Image(*value)


if __name__ == '__main__':
    toJSONFilters(filter(None, [
        baseurl_fix if BASEURL else None
    ]))
