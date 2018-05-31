from itertools import chain
from pathlib import Path

from livereload import Server, shell


server = Server()

for p in chain(Path('content').glob('**/README.org'),
               Path('scripts').glob('**'),
               Path('static').glob('**')):
    server.watch(str(p), shell('make build'))

server.serve(root='_site')
