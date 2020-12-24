# -*- coding: utf-8 -*
from socket import *
import select

class DNSQuery:
    def __init__(self, data):
        self.data=data
        self.dominio=''

        tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
        if tipo == 0:                     # Standard query
            ini=12
            lon=ord(data[ini])
            while lon != 0:
                self.dominio+=data[ini+1:ini+lon+1]+'.'
                ini+=lon+1
                lon=ord(data[ini])

# build the packet send to client
# from the Internet
    def respuesta(self, ip):
        packet=''
        if self.dominio:
            packet+=self.data[:2] + "\x81\x80"
            packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
            packet+=self.data[12:]                                         # Original Domain Name Question
            packet+='\xc0\x0c'                                             # Pointer to domain name
            packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
            packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
        return packet

def get_size(s):
	x_1 = s[0]
	x_2 = s[1]

	y_1 = [ord(c) for c in x_1]
	y_2 = [ord(c) for c in x_2]
	size = y_1[0]*256 + y_2[0]
	return size

client_proxy_socket_UDP = socket(AF_INET, SOCK_DGRAM)
client_proxy_socket_TCP = socket(AF_INET, SOCK_STREAM)

client_proxy_socket_TCP.setblocking(0)
client_proxy_address = ('', 53)
client_proxy_socket_UDP.bind(client_proxy_address)
client_proxy_socket_TCP.bind(client_proxy_address)


client_proxy_socket_TCP.listen(5)

inputs = []
outputs = []

inputs.append(client_proxy_socket_UDP)
inputs.append(client_proxy_socket_TCP)

while inputs:
	readable, writable, exceptional = select.select(inputs, [], [])
	for s in readable:
		if s == client_proxy_socket_UDP:
			data, client_address = s.recvfrom(4096)
			if data:
		    	# Create a UDP socket between proxy and server
				proxy_server_socket = socket(AF_INET, SOCK_DGRAM)
		        # send query from client to server
		        serverName = '8.8.8.8'
		        client_query = data
		        proxy_server_socket.sendto(client_query, (serverName, 53))
		        # get response from server
		        response, server_address = proxy_server_socket.recvfrom(4096)
		        #print('data')
		        if response:
					proxy_server_socket.close()
					if response[3] == '\x83':
						ip='18.220.10.65'
						p=DNSQuery(data)
						s.sendto(p.respuesta(ip), client_address)
						break
					else:
						# send response from proxy to client
						s.sendto(response, client_address)

		elif s == client_proxy_socket_TCP:
			connectionSocket, client_address_new = s.accept()
			while True:
				sentence = connectionSocket.recv(2048)
				size_1 = get_size(sentence)
				receive_len_1 = len(sentence)
				while receive_len_1<size_1+2:
					sentence += connectionSocket.recv(2048)
					receive_len_1 += len(sentence)
					#receive_len = len(sentence) 
				if sentence:
					proxy_server_socket_TCP = socket(AF_INET,SOCK_STREAM)
					proxy_server_socket_TCP.connect(('8.8.8.8', 53))
					proxy_server_socket_TCP.send(sentence)

					response_TCP = proxy_server_socket_TCP.recv(2048)
					size = get_size(response_TCP)
					print(size)
					receive_len = len(response_TCP)
					print(receive_len)
					while receive_len < size + 2:
						response_TCP += proxy_server_socket_TCP.recv(2048)
						receive_len += len(response_TCP)
					connectionSocket.sendto(response_TCP, client_address_new)
					proxy_server_socket_TCP.close()

				if len(sentence) == 0:
					connectionSocket.close()

				break


