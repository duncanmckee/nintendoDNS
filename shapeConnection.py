import socket
import sys
import os
import threading

LISTEN_COUNT = 5
SEND_PORT = 5600
RECV_PORT = 5601
ackMsg = "OK"
nackMsg = "NO"

def join_conn(start_host_name):
    current_name = start_host_name
    while True:
        current_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        current_conn.connect((current_name, RECV_PORT))
        response = current_conn.recv(1024).decode()
        # print("CONNECTING MSG:", response)
        if(response == ackMsg):
            send_conn = current_conn
            recv_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            recv_conn.connect((current_name, SEND_PORT))
            return (current_name, send_conn, recv_conn)
        elif(response == nackMsg):
            current_conn.close()
            return (None, None)
        current_name = response
        current_conn.close()

class ShapeHostPoint:
    def __init__(self, rect_handler, circ_handler):
        self.senders = []
        self.receivers = []
        self.accept_conns = True
        self.rect_handler = rect_handler
        self.circ_handler = circ_handler
        self.accept_send_thread = threading.Thread(target=self.await_send_joins, args=[])
        self.accept_send_thread.start()
        self.accept_send_thread = threading.Thread(target=self.await_recv_joins, args=[])
        self.accept_send_thread.start()
    
    def await_recv_joins(self):
        host_name = socket.gethostname()
        print("Awaiting connections at:", host_name)
        join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        join_conn.bind((host_name, RECV_PORT))
        join_conn.listen(LISTEN_COUNT)
        while(self.accept_conns):
            conn, _ = join_conn.accept()
            # print("RECV Connection")
            conn.sendall(ackMsg.encode())
            receiver = ShapeReceiver(conn, self.recv_rect, self.recv_circ)
            self.receivers.append(receiver)
            recv_thread = threading.Thread(target=receiver.recv_shape_loop, args=[])
            recv_thread.start()
    
    def await_send_joins(self):
        host_name = socket.gethostname()
        join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        join_conn.bind((host_name, SEND_PORT))
        join_conn.listen(LISTEN_COUNT)
        while(self.accept_conns):
            conn, _ = join_conn.accept()
            # print("SEND Connection")
            sender = ShapeSender(conn)
            self.senders.append(sender)
    
    def send_rect(self, x1, y1, x2, y2):
        # print("HOST SEND_RECT")
        self.rect_handler(x1, y1, x2, y2)
        for sender in self.senders:
            sender.send_rect(x1, y1, x2, y2)
    
    def recv_rect(self, x1, y1, x2, y2):
        self.send_rect(x1, y1, x2, y2)

    def send_circ(self, x, y, r):
        self.circ_handler(x, y, r)
        for sender in self.senders:
            sender.send_circ(x, y, r)
    
    def recv_circ(self, x, y, r):
        self.send_circ(x, y, r)

class ShapeJoinPoint:
    def __init__(self, start_host_name, rect_handler, circ_handler):
        (self.forward_name, send_conn, recv_conn) = join_conn(start_host_name)
        self.sender = ShapeSender(send_conn)
        self.receiver = ShapeReceiver(recv_conn, rect_handler, circ_handler)
        self.recv_thread = threading.Thread(target=self.receiver.recv_shape_loop, args=[])
        self.recv_thread.start()
        self.accept_conns = True
        self.accept_send_thread = threading.Thread(target=self.await_recv_joins, args=[])
        self.accept_send_thread.start()

    def await_recv_joins(self):
        host_name = socket.gethostname()
        join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        join_conn.bind((host_name, RECV_PORT))
        join_conn.listen(LISTEN_COUNT)
        while(self.accept_conns):
            conn, _ = join_conn.accept()
            conn.sendall(self.forward_name.encode())
            conn.close()
    
    def send_rect(self, x1, y1, x2, y2):
        # print("JOIN SEND_RECT")
        self.sender.send_rect(x1, y1, x2, y2)

    def send_circ(self, x, y, r):
        self.sender.send_circ(x, y, r)

class ShapeEndPoint:
    def __init__(self, start_host_name, rect_handler, circ_handler):
        (_, send_conn, recv_conn) = join_conn(start_host_name)
        # print("END CONNECTED")
        self.sender = ShapeSender(send_conn)
        self.receiver = ShapeReceiver(recv_conn, rect_handler, circ_handler)
        self.recv_thread = threading.Thread(target=self.receiver.recv_shape_loop, args=[])
        self.recv_thread.start()
    
    def send_rect(self, x1, y1, x2, y2):
        # print("END SEND_RECT")
        self.sender.send_rect(x1, y1, x2, y2)

    def send_circ(self, x, y, r):
        self.sender.send_circ(x, y, r)

class ShapeSender:
    def __init__(self, conn):
        # print("START SENDER")
        self.conn = conn
    
    def send_rect(self, x1, y1, x2, y2):
        # print("SENDER SEND_RECT")
        if(not self.send_msg("RECT")):
            print("Fail 0")
            return False
        msg = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)
        if(not self.send_msg(str(len(msg)))):
            print("Fail 1")
            return False
        if(not self.send_msg(msg)):
            print("Fail 2")
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
    def __init__(self, conn, rect_handler, circ_handler):
        # print("START RECEIVER")
        self.conn = conn
        self.rect_handler = rect_handler
        self.circ_handler = circ_handler
    
    def recv_shape_loop(self):
        self.run_loop = True
        while self.run_loop:
            self.recv_shape()

    def recv_shape(self):
        shape_type = self.conn.recv(1024).decode()
        # print("RECEIVER GOT:", shape_type)
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
        # print("LENGTH:",length)
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
        self.send_ack()
        self.rect_handler(x1, y1, x2, y2)

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
        self.send_ack()
        self.circ_handler(x, y, r)

    def send_ack(self):
        self.conn.sendall(ackMsg.encode())
    
    def send_nack(self):
        try:
            self.conn.sendall(nackMsg.encode())
        except:
            return