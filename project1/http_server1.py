#!/usr/bin/env python
from socket import*
import socket
import re
import sys

host = ""
port = raw_input()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, int(port)))

server_socket.listen(5)

f = open('rfc2616.html', 'r')
index_content = '''
HTTP/1.1 200 ok
Content-Type: text/html
'''
index_content += f.read()
f.close()

while True:
    connection_Socket, addr = server_socket.accept()
    data = connection_Socket.recv(1024)
    method = data.split(' ')[0]
    scr = data.split(' ')[1]

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
    connection_Socket.sendall(response)
    connection_Socket.close()

