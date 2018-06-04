from itertools import chain
import json
from os.path import join
from pathlib import Path
from urllib.parse import urlparse

from livereload import Server, shell
from livereload.handlers import LiveReloadHandler


work_paths = set()
on_message = LiveReloadHandler.on_message


def on_message_ex(self, message):
    # Intercept the event and record the working path
    url = json.loads(message).get('url')
    if url is not None:
        path = urlparse(url).path
        # Remove leadling '/'
        work_paths.add(path[1:])

    # Call the original one
    return on_message(self, message)


LiveReloadHandler.on_message = on_message_ex


def touch():
    if work_paths:
        work_files = [join('content', p, 'README.org') for p in work_paths]
        targets = ' '.join(f"'{f}'" for f in work_files)
        shell(f'touch {targets}')()


server = Server()

for p in chain(Path('scripts').glob('**'),
               Path('static').glob('**')):
    server.watch(str(p), touch)

for p in chain(Path('content').glob('**/README.org')):
    server.watch(str(p), shell('make local'))

server.serve(root='_site')
