import socket
import sys
import subprocess


def get_host():
    command = "ifconfig en0 | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/'"
    result = subprocess.check_output(command, shell=True)
    HOST = result.decode('utf-8')[:-2]  # Remove \n
    return HOST


TCP_HOST = get_host()
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
