import socket
import sys
import os

defaultPort = 5600

def client_program():
    port = defaultPort
    if(len(sys.argv) == 3):
        port = int(sys.argv[2])
    elif(len(sys.argv) != 2):
        print("Usage: python client.py <server_IP_address> <server_port_number>")
        sys.exit()
    server_addr = (sys.argv[1], port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_addr)

    send_rect(client_socket,0,0,10,10)

def send_rect(client_socket, x1, y1, x2, y2):
    client_socket.sendall("RECT".encode()) 
    if(client_socket.recv(2).decode() != "OK"):
        return False
    command_args = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)
    client_socket.sendall(str(len(command_args)).encode())
    if(client_socket.recv(2).decode() != "OK"):
        return False
    client_socket.sendall(command_args.encode())
    if(client_socket.recv(2).decode() != "OK"):
        return False
    return True

if __name__ == '__main__':
    client_program()