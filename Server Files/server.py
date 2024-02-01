import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('', 3389)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(2)

print('Server is listening on {}:{}'.format(*server_address))

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive and send back data
    data = client_socket.recv(1024)
    print('Received data: {!r}'.format(data.decode('utf-8')))
    client_socket.sendall(data)
    print("Closing")
    client_socket.close()
# use thread pooling,caching to make data sending faster and efficient