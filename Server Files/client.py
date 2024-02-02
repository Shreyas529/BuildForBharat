import socket
import time
start=time.time()
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's address and port
address="34.125.204.13"
address=""
server_address = (address, 3389)
client_socket.connect(server_address)

# Send data to the server
message = '2134'
print('Sending data: {!r}'.format(message))
client_socket.sendall(message.encode('utf-8'))

# Receive the response from the server
data = client_socket.recv(1024)
# print('Received data from server: {!r}'.format(data.decode('utf-8')))
print(data.decode("utf-8"))
# Clean up the connection
print('Closing connection...')
client_socket.close()
end=time.time()
print("Time taken:",end-start)
