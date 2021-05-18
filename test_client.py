import socket

host = '137.112.136.71'
port = 5602
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))