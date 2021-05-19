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
    def __init__(self, host_name):
        self.host_name = host_name
        self.senders = []
        self.receivers = []
        self.accept_conns = True
        self.closing = False
        self.rectangle_handler = None
        self.ellipse_handler = None
        self.line_handler = None
        self.accept_send_thread = threading.Thread(target=self.await_send_joins, args=[])
        self.accept_send_thread.start()
        self.accept_send_thread = threading.Thread(target=self.await_recv_joins, args=[])
        self.accept_send_thread.start()
    
    def await_recv_joins(self):
        print("Awaiting connections at:", self.host_name)
        recv_join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_join_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv_join_conn.bind((self.host_name, RECV_PORT))
        recv_join_conn.listen(LISTEN_COUNT)
        while(self.accept_conns):
            conn, _ = recv_join_conn.accept()
            if(not self.accept_conns):
                recv_join_conn.close()
                return
            conn.sendall(ackMsg.encode())
            receiver = ShapeReceiver(conn)
            receiver.set_rectangle_handler(self.recv_rectangle)
            receiver.set_ellipse_handler(self.recv_ellipse)
            receiver.set_line_handler(self.recv_line)
            receiver.set_close_handler(self.close_handler)
            self.receivers.append(receiver)
            recv_thread = threading.Thread(target=receiver.recv_shape_loop, args=[])
            recv_thread.start()
    
    def await_send_joins(self):
        send_join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_join_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        send_join_conn.bind((self.host_name, SEND_PORT))
        send_join_conn.listen(LISTEN_COUNT)
        while(self.accept_conns):
            conn, _ = send_join_conn.accept()
            if(not self.accept_conns):
                send_join_conn.close()
                return
            sender = ShapeSender(conn)
            self.senders.append(sender)

    def send_rectangle(self, x1, y1, x2, y2, width, color):
        if(self.rectangle_handler != None):
            self.rectangle_handler(x1, y1, x2, y2, width, color)
        for sender in self.senders:
            sender.send_rectangle(x1, y1, x2, y2, width, color)
    
    def send_ellipse(self, x1, y1, x2, y2, width, color):
        if(self.ellipse_handler != None):
            self.ellipse_handler(x1, y1, x2, y2, width, color)
        for sender in self.senders:
            sender.send_ellipse(x1, y1, x2, y2, width, color)

    def send_line(self, x1, y1, x2, y2, width, color):
        if(self.line_handler != None):
            self.line_handler(x1, y1, x2, y2, width, color)
        for sender in self.senders:
            sender.send_line(x1, y1, x2, y2, width, color)
    
    def recv_rectangle(self, x1, y1, x2, y2, width, color):
        self.send_rectangle(x1, y1, x2, y2, width, color)

    def recv_ellipse(self, x1, y1, x2, y2, width, color):
        self.send_ellipse(x1, y1, x2, y2, width, color)

    def recv_line(self, x1, y1, x2, y2, width, color):
        self.send_line(x1, y1, x2, y2, width, color)
    
    def set_rectangle_handler(self, rectangle_handler):
        self.rectangle_handler = rectangle_handler
    
    def set_ellipse_handler(self, ellipse_handler):
        self.ellipse_handler = ellipse_handler
    
    def set_line_handler(self, line_handler):
        self.line_handler = line_handler
    
    def close_handler(self, closed_receiver):
        index = 0
        while index < len(self.receivers):
            if(self.receivers[index] == closed_receiver):
                if(not self.closing):
                    self.senders[index].send_close()
                self.receivers.pop(index)
                self.senders.pop(index)
                return
    
    def close(self):
        self.accept_conns = False
        self.closing = True
        for sender in self.senders:
            sender.send_close()
        close_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_recv.connect((self.host_name, RECV_PORT))
        close_recv.close()
        close_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_send.connect((self.host_name, SEND_PORT))
        close_send.close()

class ShapeJoinPoint:
    def __init__(self, start_host_name):
        (self.forward_name, send_conn, recv_conn) = join_conn(start_host_name)
        self.sender = ShapeSender(send_conn)
        self.receiver = ShapeReceiver(recv_conn)
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
    
    def send_rectangle(self, x1, y1, x2, y2):
        self.sender.send_rectangle(x1, y1, x2, y2)

    def send_ellipse(self, x1, y1, x2, y2):
        self.sender.send_ellipse(x1, y1, x2, y2)
    
    def send_line(self, x1, y1, x2, y2):
        self.sender.send_line(x1, y1, x2, y2)
    
    def set_rectangle_handler(self, rectangle_handler):
        self.receiver.set_rectangle_handler(rectangle_handler)
    
    def set_ellipse_handler(self, ellipse_handler):
        self.receiver.set_ellipse_handler(ellipse_handler)

    def set_line_handler(self, line_handler):
        self.receiver.set_line_handler(line_handler)
    
    def close(self):
        print("Close")

class ShapeEndPoint:
    def __init__(self, start_host_name):
        (_, send_conn, recv_conn) = join_conn(start_host_name)
        self.sender = ShapeSender(send_conn)
        self.receiver = ShapeReceiver(recv_conn)
        self.receiver.set_close_handler(self.close_handler)
        self.recv_thread = threading.Thread(target=self.receiver.recv_shape_loop, args=[])
        self.recv_thread.start()
    
    def send_rectangle(self, x1, y1, x2, y2, width, color):
        if(self.sender):
            self.sender.send_rectangle(x1, y1, x2, y2, width, color)

    def send_ellipse(self, x1, y1, x2, y2, width, color):
        if(self.sender):
            self.sender.send_ellipse(x1, y1, x2, y2, width, color)

    def send_line(self, x1, y1, x2, y2, width, color):
        if(self.sender):
            self.sender.send_line(x1, y1, x2, y2, width, color)
    
    def set_rectangle_handler(self, rectangle_handler):
        if(self.receiver):
            self.receiver.set_rectangle_handler(rectangle_handler)
    
    def set_ellipse_handler(self, ellipse_handler):
        if(self.receiver):
            self.receiver.set_ellipse_handler(ellipse_handler)
    
    def set_line_handler(self, line_handler):
        if(self.receiver):
            self.receiver.set_line_handler(line_handler)
    
    def close_handler(self, closed_receiver):
        if(self.sender):
            self.sender.send_close()
            self.sender = None
        self.receiver = None

    def close(self):
        if(self.sender):
            self.sender.send_close()
            self.sender = None

class ShapeSender:
    def __init__(self, conn):
        self.conn = conn
    
    def send_rectangle(self, x1, y1, x2, y2, width, color):
        if(not self.send_msg("RECT")):
            print("Fail 0")
            return False
        msg = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)+"|"+str(width)+"|"+str(color)
        if(not self.send_msg(str(len(msg)))):
            print("Fail 1")
            return False
        if(not self.send_msg(msg)):
            print("Fail 2")
            return False
        return True

    def send_ellipse(self, x1, y1, x2, y2, width, color):
        if(not self.send_msg("ELIP")):
            return False
        msg = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)+"|"+str(width)+"|"+str(color)
        if(not self.send_msg(str(len(msg)))):
            return False
        if(not self.send_msg(msg)):
            return False
        return True
    
    def send_line(self, x1, y1, x2, y2, width, color):
        if(not self.send_msg("LINE")):
            return False
        msg = str(x1)+"|"+str(y1)+"|"+str(x2)+"|"+str(y2)+"|"+str(width)+"|"+str(color)
        if(not self.send_msg(str(len(msg)))):
            return False
        if(not self.send_msg(msg)):
            return False
        return True

    def send_close(self):
        if(not self.send_msg("CLOSE")):
            return False
        self.conn.close()
        return True

    def send_msg(self, msg):
        self.conn.sendall(msg.encode())
        if(self.conn.recv(2).decode() == ackMsg):
            return True
        return False

class ShapeReceiver:
    def __init__(self, conn):
        self.conn = conn
        self.rectangle_handler = None
        self.ellipse_handler = None
        self.line_handler = None
        self.close_handler = None
    
    def recv_shape_loop(self):
        self.run_loop = True
        while self.run_loop:
            self.recv_shape()

    def recv_shape(self):
        shape_type = self.conn.recv(1024).decode()
        if(shape_type == "RECT"):
            self.send_ack()
            self.recv_rectangle()
        elif(shape_type == "ELIP"):
            self.send_ack()
            self.recv_ellipse()
        elif(shape_type == "LINE"):
            self.send_ack()
            self.recv_line()
        elif(shape_type == "CLOSE"):
            self.send_ack()
            self.close()
            if(self.close_handler):
                self.close_handler(self)
        else:
            self.send_nack()
    
    def recv_rectangle(self):
        length = int(self.conn.recv(1024).decode())
        self.send_ack()
        data = self.conn.recv(length+1).decode()
        args = data.split("|")
        if(len(args)!=6):
            self.send_nack()
            return
        x1 = int(args[0])
        y1 = int(args[1])
        x2 = int(args[2])
        y2 = int(args[3])
        width = int(args[4])
        color = int(args[5])
        self.send_ack()
        if(self.rectangle_handler):
            self.rectangle_handler(x1, y1, x2, y2, width, color)

    def recv_ellipse(self):
        length = int(self.conn.recv(1024).decode())
        self.send_ack()
        data = self.conn.recv(length+1).decode()
        args = data.split("|")
        if(len(args)!=6):
            self.send_nack()
            return
        x1 = int(args[0])
        y1 = int(args[1])
        x2 = int(args[2])
        y2 = int(args[3])
        width = int(args[4])
        color = int(args[5])
        self.send_ack()
        if(self.ellipse_handler):
            self.ellipse_handler(x1, y1, x2, y2, width, color)

    def recv_line(self):
        length = int(self.conn.recv(1024).decode())
        self.send_ack()
        data = self.conn.recv(length+1).decode()
        args = data.split("|")
        if(len(args)!=6):
            self.send_nack()
            return
        x1 = int(args[0])
        y1 = int(args[1])
        x2 = int(args[2])
        y2 = int(args[3])
        width = int(args[4])
        color = int(args[5])
        self.send_ack()
        if(self.line_handler):
            self.line_handler(x1, y1, x2, y2, width, color)

    def set_rectangle_handler(self, rectangle_handler):
        self.rectangle_handler = rectangle_handler
    
    def set_ellipse_handler(self, ellipse_handler):
        self.ellipse_handler = ellipse_handler

    def set_line_handler(self, line_handler):
        self.line_handler = line_handler
    
    def set_close_handler(self, close_handler):
        self.close_handler = close_handler

    def send_ack(self):
        self.conn.sendall(ackMsg.encode())
    
    def send_nack(self):
        try:
            self.conn.sendall(nackMsg.encode())
        except:
            return
    
    def close(self):
        self.run_loop = False
        self.conn.close()