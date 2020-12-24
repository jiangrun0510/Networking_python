#!/usr/bin/env python
from socket import*
import socket
import re
import select
import sys

server_address = ('', 9031)
inputs = []
outputs = []

f = open('rfc2616.html', 'r')
index_content = '''
HTTP/1.1 200 ok
Content-Type: text/html
'''
index_content += f.read()
f.close()

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # from Internet
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(server_address)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    server_socket.listen(5)

    #from Internet
    server_socket.setblocking(False)

    inputs.append(server_socket)

    while True:
        # from Internet
        readable, writable, exceptional = select.select(inputs, [], [])

        for client in readable:

            if client == server_socket:
                connection_Socket, addr = server_socket.accept()
                print >>sys.stderr, 'new connection from', addr
                inputs.append(connection_Socket)

            else:
                data = client.recv(1024)
                method = data.split(' ')[0]
                scr = data.split(' ')[1]
                response = ''
                if method == 'GET':
                    if re.match(r'/(.*).html', data) != "None" or re.match(r'/(.*).htm', data) != "None":
                        path = scr.split('/')[1]
                        if path == "rfc2616.html":
                            response = index_content

                    else:
                        response = '''
                        HTTP/1.1 403 Forbidden
                        '''
                else:
                    response = '''
                    HTTP/1.1 404 Not Found
                    '''
                # print client, response
                client.send(response)
                client.close()
                inputs.remove(client)
