from itertools import chain
import json
from os.path import join
from pathlib import Path
from urllib.parse import urlparse

from livereload import Server, shell
from livereload.handlers import LiveReloadHandler


work_paths = set()


def make():
    shell('make local')()


def refresh():
    if work_paths:
        work_files = [join('content', p, 'README.org') for p in work_paths]
        targets = ' '.join(f"'{f}'" for f in work_files)
        shell(f'touch {targets}')()
    else:
        make()


on_message = LiveReloadHandler.on_message


def on_message_ex(self, message):
    # Intercept the event and record the working path
    url = json.loads(message).get('url')
    if url is not None:
        # Remove leadling '/'
        path = urlparse(url).path[1:]
        if path and path not in work_paths:
            work_paths.add(path)
            refresh()

    # Call the original one
    return on_message(self, message)


LiveReloadHandler.on_message = on_message_ex


server = Server()

for p in chain(Path('scripts').glob('**/*'),
               Path('templates').glob('**/*'),
               Path('includes').glob('**/*'),
               Path('static').glob('**/*'),
               Path('.').glob('Makefile')):
    server.watch(str(p), refresh)

for p in chain(Path('content').glob('**/README.org')):
    server.watch(str(p), make)

server.serve(root='_site')
