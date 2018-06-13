from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape


def make_breadcrumb(target):
    segments = ('',) + Path(target).parts[1:-1]
    segments = list(segments)

    hrefs = []
    for seg in segments:
        prev = hrefs[-1] if hrefs else ''
        href = f'{prev}{seg}/'
        hrefs.append(href)

    # Specialize the first and last
    segments[0] = 'Home'
    hrefs[-1] = None

    assert(len(segments) == len(hrefs))
    return zip(hrefs, segments)


def make_children(target):
    context = Path(target).parts[1:-1]
    # skip making child links for /index.html
    if not context:
        return []
    src = Path('content', *context)
    names = [p.parent.relative_to(src)
             for p in src.glob('*/README.org')]
    return sorted(names)


env = Environment(loader=FileSystemLoader('resources'),
                  autoescape=select_autoescape(['html']))

template = env.get_template('nav.html')


TARGET = sys.argv[1]


with open(TARGET, 'w') as f:
    rendered = template.render(breadcrumb=make_breadcrumb(TARGET),
                               children=make_children(TARGET))
    f.write(rendered)
