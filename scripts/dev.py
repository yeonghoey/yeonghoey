from pathlib import Path

from livereload import Server, shell


server = Server()
for p in Path('content').glob('**/README.org'):
    server.watch(str(p), shell('make'))
server.serve()
