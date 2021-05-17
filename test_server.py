import socket

print("byname(hostname):",socket.gethostbyname(socket.gethostname()))
print("byname(localhost):",socket.gethostbyname('localhost'))
print("byaddr('137.112.136.71'):",socket.gethostbyaddr('137.112.136.71'))
print("byaddr(byname(hostname)):",socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))


host = socket.gethostbyname(socket.gethostname())
host = socket.gethostbyname('localhost')
host = '137.112.136.71'
port = 5602
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_address = (host, port)
print(host_address)
server_socket.bind((host, port))
server_socket.listen(2)
conn, address = server_socket.accept()
print(address)
conn.close()
server_socket.close()