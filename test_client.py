import socket

host = '127.0.0.1'
port = 5600
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))