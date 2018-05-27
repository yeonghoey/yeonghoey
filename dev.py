from livereload import Server, shell

server = Server()
server.watch('content/**/*', shell('make'))
server.serve(root='docs')
