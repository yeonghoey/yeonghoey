from os import environ
from os.path import dirname, splitext
from pprint import pprint
import re
from sys import stderr
from textwrap import dedent

import pandocfilters as pf


DEBUG = environ.get('YEONGHOEY_FILTER_DEBUG') is not None

SRC = environ['YEONGHOEY_FILTER_SRC']
MEDIA = environ.get('YEONGHOEY_FILTER_MEDIA')

# =============================================================================
# URL fix utils
# =============================================================================
CONTEXT = re.sub(r'^content/', '', dirname(SRC))


def media(url):
    return absurl(url, base=MEDIA)


def absurl(url, base=None):
    return '/'.join([base or '', CONTEXT, url])


# =============================================================================
# Handle functions
# =============================================================================
# When `handle_<function>` returns:
# pf.Foo : replace (spans as spans, divs as divs only)
#   None : do nohting
#     [] : delete
# =============================================================================


# =============================================================================
# Print handler parameters
# FIXME: Is there any clear way?
# =============================================================================
def handle_debug(*args):
    print(file=stderr)
    names = 'key value format meta'.split()
    for n, a in zip(names, args):
        print(f'{n:6}: ', end='', file=stderr)
        pprint(a, indent=4, stream=stderr)
    print(file=stderr)


# =============================================================================
# Fix url for images
# FIXME: process only relative link images
# =============================================================================
def handle_image(key, value, format, meta):
    if key == 'Image':
        attr, inlines, target = value
        url, title = target
        return pf.Image(attr, inlines, (media(url), title))


# =============================================================================
# Remove org-tags like :TOC_2_gh:
# =============================================================================
def handle_notag(key, value, format, meta):
    if key == 'Span':
        attr, inlines = value
        _, classes, _ = attr
        if 'tag' in classes:
            return []


# =============================================================================
# Embed pdf files, use `[[file:<path>.pdf::<ratio>]]`
# <ratio> is one of `21by9`, `16by9`, `4by3` `1by1
# =============================================================================
def handle_pdf(key, value, format, meta):
    assert format == 'html'
    if key == 'Link':
        attr, inlines, target = value
        url, title = target
        src, _, ratio = url.rpartition('::')
        _, ext = splitext(src)
        if ext == '.pdf' and ratio in ('16by9', '4by3'):
            src = media(src)
            return pf.RawInline(format, dedent(f'''\
            <div class="embed embed-{ratio}">
                <iframe src="{src}"
                        type="application/pdf"
                        allowfullscreen>
                <a href="{src}">{src}</a>
                </iframe>
            </div>
            '''))


# =============================================================================


if __name__ == '__main__':
    pf.toJSONFilters(filter(None, [
        handle_debug if DEBUG else None,
        handle_image,
        handle_notag,
        handle_pdf,
    ]))
