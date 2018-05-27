from copy import deepcopy
import os

from pandocfilters import Image, toJSONFilters


SRC_PATH = os.environ['YHY_SRC_PATH']
BASE_URL = os.environ['YHY_BASE_URL']

SRC_DIR = os.path.dirname(SRC_PATH)


def baseurl_fix(key, value, format, meta):
    if key == 'Image':
        _, _, (url, _) = value
        new_ = deepcopy(value)
        new_[2][0] = '/'.join([BASE_URL, SRC_DIR, url])
        return Image(*new_)


if __name__ == '__main__':
    toJSONFilters([
        baseurl_fix,
    ])
