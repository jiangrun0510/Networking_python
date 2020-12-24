#!/usr/bin/env python
import socket
import sys
import urlparse
input = raw_input()

scheme = urlparse.urlparse(input).scheme
path = urlparse.urlparse(input).path
netloc = urlparse.urlparse(input).netloc
if path  == '':
    path = '/'

def Get_status_code():
    client_request = 'GET '+path+' HTTP/1.1\r\nHost:'+netloc+'\r\nConnection: close\r\n\r\n'
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((netloc,80))
    s.send(client_request)
    buffer = []
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = ''.join(buffer)
    s.close()
    header, html = data.split('\r\n\r\n', 1)
    status_code = int(header[9:12])
    return header, status_code, html

header, status_code, html = Get_status_code()

def Relocation():
    relocation = header.split('Location: ', 1)[1].split('\r\n', 1)[0]
    netloc = urlparse.urlparse(relocation).netloc
    scheme = urlparse.urlparse(relocation).scheme
    path = urlparse.urlparse(relocation).path
    if path =='':
         path ='/'
    return netloc, scheme, path

if status_code != 404:
    if status_code == 301 or 302:
        n=0
        while n <= 10 and status_code != 403:
            if status_code == 301 or 302 and status_code != 200:
                netloc, scheme, path = Relocation()
                header, status_code, html = Get_status_code()
                n = n+1
                print >>sys.stderr, 'Redirected to ' + netloc+path
                if scheme == 'https':
                    break
                if n == 11:
                    sys.exit(1)

            else:
                break



if scheme == 'http' and status_code == 200 or status_code >= 400:
    if header.find('text.html'):
        print >>sys.stdout, html
    else:
        sys.exit(1)
    if status_code == 200:
        sys.exit(0)
    if status_code >=400:
        sys.exit(1)
elif scheme == 'https':
    sys.exit(1)

elif scheme =='':
    sys.exit(1)

