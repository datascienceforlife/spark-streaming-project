import socket
import sys

TCP_HOST = "172.22.224.79" # To be substitued with the IP address on the network
TCP_PORT = 9999
FILE_PATH = "./data.txt"

with open(FILE_PATH, 'r') as content_file:
    data = content_file.read()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (TCP_HOST, TCP_PORT)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print('Listening on {}:{}...'.format(TCP_HOST, TCP_PORT))
print('Waiting for connection')
connection, client_address = sock.accept()
try:		
	connection.sendall(data.encode())
    
finally:
  # Clean up the connection
  connection.close()	  
