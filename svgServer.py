import socket
import sys
import os

defaultPort = 5600

def server_program():
    # get the hostname and print it
    host = socket.gethostname()
    print("Host name: " + str(host))
    buf = 1024
    port = defaultPort
    if(len(sys.argv) == 2):
        port = int(sys.argv[1])
    elif(len(sys.argv) != 1):
        print("Usage: python server.py <port_number>")
        sys.exit()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))


    data = conn.recv(1024).decode()
    print(data)
    conn.sendall("OK".encode())
    data = conn.recv(1024).decode()
    print(data)
    conn.sendall("OK".encode())
    data = conn.recv(1024).decode()
    print(data)
    conn.sendall("OK".encode())


if __name__ == '__main__':
    server_program()