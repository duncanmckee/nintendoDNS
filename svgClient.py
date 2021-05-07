import socket
import sys
import os
from shapeConnection import ShapeSender

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

    sender = ShapeSender(client_socket)
    sender.send_rect(0,0,10,10)
    sender.send_circ(5,-3,10)

if __name__ == '__main__':
    client_program()