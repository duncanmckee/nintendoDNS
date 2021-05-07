import socket
import sys
import os

ackMsg = "OK"
nackMsg = "NO"

class ShapeSender:
    def __init__(self, conn):
        self.conn = conn
    
    def send_rect(self, x1, y1, x2, y2):
        if(not self.send_msg("RECT")):
            return False
        msg = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)
        if(not self.send_msg(str(len(msg)))):
            return False
        if(not self.send_msg(msg)):
            return False
        return True

    def send_circ(self, x, y, r):
        if(not self.send_msg("CIRC")):
            return False
        msg = str(x)+"|"+str(y)+"|"+str(r)
        if(not self.send_msg(str(len(msg)))):
            return False
        if(not self.send_msg(msg)):
            return False
        return True

    def send_msg(self, msg):
        self.conn.sendall(msg.encode())
        if(self.conn.recv(2).decode() == ackMsg):
            return True
        return False

class ShapeReceiver:
    def __init__(self, conn):
        self.conn = conn
    
    def recv_shape(self):
        shape_type = self.conn.recv(1024).decode()
        if(shape_type == "RECT"):
            self.send_ack()
            self.recv_rect()
        elif(shape_type == "CIRC"):
            self.send_ack()
            self.recv_circ()
        else:
            self.send_nack()
    
    def recv_rect(self):
        length = int(self.conn.recv(1024).decode())
        self.send_ack()
        data = self.conn.recv(length+1).decode()
        args = data.split("|")
        if(len(args)!=4):
            self.send_nack()
            return
        x1 = int(args[0])
        y1 = int(args[1])
        x2 = int(args[2])
        y2 = int(args[3])
        print("Rect: (" + str(x1) + ", " + str(y1) + ") -> (" + str(x2) + ", " + str(y2) + ")")
        self.send_ack()

    def recv_circ(self):
        length = int(self.conn.recv(1024).decode())
        self.send_ack()
        data = self.conn.recv(length+1).decode()
        args = data.split("|")
        if(len(args)!=3):
            self.send_nack()
            return
        x = int(args[0])
        y = int(args[1])
        r = int(args[2])
        print("Circ: R: " + str(r) + " @ (" + str(x) + ", " + str(y) + ")")
        self.send_ack()

    def send_ack(self):
        self.conn.sendall(ackMsg.encode())
    
    def send_nack(self):
        self.conn.sendall(nackMsg.encode())