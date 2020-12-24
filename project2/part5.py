from socket import*
import select

inputs = []
outputs = []

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 80))
server_socket.listen(5)
server_socket.setblocking(False)

inputs.append(server_socket)

while True:
	readable, writable, exceptional = select.select(inputs, [], [])
	for client in readable:
		if client == server_socket:
			connection_socket, addr = server_socket.accept()
			inputs.append(connection_socket)

		else:
			data = client.recv(1024)
			if 'Host' not in data:
				print data
				pass
			else:
				a = data.split('Host:')[1]
				netloc = a.split('\r\n')[0]
				advertisement = '''
				<!DOCTYPE html>
				<html>
				<body>
				    
				<p>I see you were looking for: %s, </p >
				<p>but wouldn't you rather buy that from <a href="https://world.taobao.com" title="The Taobao homepage" target="_blank">taobao.com</a >.</p >
				</body>
				</html>'''%(netloc)
				client.sendall(advertisement)
				client.close()
				inputs.remove(client)