#!/usr/bin/env python
from socket import *
import sys


# Create a UDP socket between client and proxy
client_proxy_socket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to the port
client_proxy_address = ('', 53)

client_proxy_socket.bind(client_proxy_address)
#client_proxy_socket.settimeout(1)
print('1')
# get query from client
while True:
    data, client_address = client_proxy_socket.recvfrom(4096)
    print('1')
    if data:
        # Create a UDP socket between proxy and server
        proxy_server_socket = socket(AF_INET, SOCK_DGRAM)

        # send query from client to server
        serverName = '8.8.8.8'
        client_query = data
        print(client_query)
        proxy_server_socket.sendto(client_query, (serverName, 53))

        # get response from server
        response, server_address = proxy_server_socket.recvfrom(4096)
    if response:
        print(response)
    proxy_server_socket.close()

    # send response from proxy to client
    client_proxy_socket.sendto(response, client_address)
