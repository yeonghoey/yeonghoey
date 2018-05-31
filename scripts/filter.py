from os import environ
from os.path import dirname
from pprint import pprint
import re
from sys import stderr
from textwrap import dedent

import pandocfilters as pf


BASE = environ['YEONGHOEY_FILTER_BASE']
DEBUG = environ.get('YEONGHOEY_FILTER_DEBUG') is not None
SRC = environ['YEONGHOEY_FILTER_SRC']

# =============================================================================
# Common utils for filtering
# =============================================================================
CONTEXT_PATH = re.sub(r'^content/', '', dirname(SRC))


def basepath(url):
    if BASE:
        return '/'.join([BASE, CONTEXT_PATH, url])
    else:
        return url


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
# Fix basepath for images
# FIXME: process only relative link images
# =============================================================================
def handle_image(key, value, format, meta):
    if key == 'Image':
        attr, inlines, target = value
        url, title = target
        return pf.Image(attr, inlines, (basepath(url), title))


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
# Embed pdf files, customized syntax is following:
# <ratio> is one of `21by9`, `4by3`, `4by3` `1by1
# : YEONGHOEY_PDF[<ratio>] <src>
# =============================================================================
YEONGHOEY_PDF = re.compile(r'''^YEONGHOEY_PDF
                               \[(?P<ratio>[^]]+)\]
                               [ ]
                               (?P<src>.+)$''', re.VERBOSE)


def handle_pdf(key, value, format, meta):
    assert format == 'html'
    if key == 'CodeBlock':
        attr, code = value

        match = YEONGHOEY_PDF.match(code)
        if match is not None:
            d = match.groupdict()
            src = basepath(d['src'])
            ratio = d['ratio']
            return pf.RawBlock(format, dedent(f'''\
            <div class="w-75 embed-responsive embed-responsive-{ratio}">
                <iframe class="embed-responsive-item"
                        src="/ViewerJS/#{src}"
                        type="application/pdf"
                        allowfullscreen
                        webkitallowfullscreen>
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
