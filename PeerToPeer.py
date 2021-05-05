import socket
import struct
import threading
import time

class PeerToPeer:
    def __init__(self, max_peers, server_port, my_id=None, server_host = None):
        self.max_peers = max_peers
        self.server_port = server_port
        if server_host:
            self.server_host = server_host
        else:
            self.__init_server_host()
        
        if my_id:
            self.my_id = my_id
        else:
            self.my_id = '%s:%d' % (self.server_host, self.server_port)
        
        self.peer_lock = threading.Lock()
        self.peers = {}
        self.shutdown = False

        self.handlers = {}
        self.router = None
    
    def __init_server_host(self):
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.connect( ( "www.google.com", 80 ) )
        self.serverhost = s.getsockname()[0]
        s.close()

    def __handle_peer(self, client_sock):
        host, port = client_sock.getpeername()
        peer_con = PeerConnection(None, host, port, client_sock)

        try:
            msg_type, msg_data = peer_con.recv_data()
            if msg_type:
                msg_type = msg_type.upper()
            if msg_type in self.handlers:
                self.handlers[msg_type](peer_con, msg_data)
        except KeyboardInterrupt:
            raise
        peer_con.close()

    def __run_stabilizer(self, stabilizer, delay):
        while not self.shutdown:
            stabilizer()
            time.sleep(delay)
    
    def set_my_id(self, my_id):
        self.my_id = my_id
    
    def start_stabilizer(self, stabilizer, delay):
        t = threading.Thread(target=self.__run_stabilizer, args=[stabilizer,delay])
        t.start()

    def add_handler(self, msg_type, handler):
        self.handlers[msg_type] = handler

    def add_router(self, router):
        self.router = router

    def add_peer(self, peer_id, host, port):
        if peer_id not in self.peers and (self.max_peers == 0 or len(self.peers) < self.max_peers):
            self.peers[peer_id] = (host, int(port))
            return True
        else:
            return False
    
    def get_peer(self, peer_id):
        return self.peers[peer_id]

    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            del self.peers[peer_id]
    
    def get_peer_ids(self):
        return self.peers.keys()
    
    def number_of_peers(self):
        return len(self.peers)
    
    def max_peers_reached(self):
        return self.max_peers > 0 and len(self.peers) == self.max_peers

    def make_server_socket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s
    
    def send_to_peer(self, peer_id, msg_type, msg_data, wait_reply=True):
        if self.router:
            next_pid, host, port = self.router(peer_id)
        if not self.router or not next_pid:
            return None
        return self.connect_and_send(host, port, msg_type, msg_data, pid=next_pid, wait_reply=wait_reply)

    def connect_and_send(self, host, port, msg_type, msg_data, pid=None, wait_reply=True):
        msg_reply = []
        try:
            peer_conn = PeerConnection(pid, host, port)
            peer_conn.send_data(msg_type, msg_data)
            if wait_reply:
                one_reply = peer_conn.recv_data()
                while(one_reply != (None, None)):
                    msg_reply.append(one_reply)
                    one_reply = peer_conn.recv_data()
            peer_conn.close()
        except KeyboardInterrupt:
            raise
        return msg_reply

    def check_live_peers(self):
        to_delete = []
        for pid in self.peers:
            is_connected = False
            try:
                host, port = self.peers[pid]
                peer_conn = PeerConnection(pid, host, port)
                peer_conn.send_data('PING','')
                is_connected = True
            except:
                to_delete.append(pid)
                if is_connected:
                    peer_conn.close()
        self.peer_lock.acquire()
        try:
            for pid in to_delete:
                if pid in self.peers:
                    del self.peers[pid]
        finally:
            self.peer_lock.release()

    def run(self):
        s = self.make_server_socket(self.server_port)
        s.settimeout(2)

        while not self.shutdown:
            try:
                client_sock, client_addr = s.accept()
                client_sock.settimeout(None)
                t = threading.Thread(target=self.__handle_peer, args=[client_sock])
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
        s.close()

class PeerConnection:
    def __init__(self, peer_id, host, port, sock=None):
        self.id = peer_id
        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock
        self.sd = self.s.makefile('rw',0)

    def __make_msg(self, msg_type, msg_data):
        msg_len = len(msg_data)
        msg = struct.pack("!4sL%ds" % msg_len, msg_type, msg_len, msg_data)
        return msg
    
    def send_data(self, msg_type, msg_data):
        try:
            msg = self.__make_msg(msg_type, msg_data)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        return True
    
    def recv_data(self):
        try:
            msg_type = self.sd.read(4)
            if not msg_type:
                return (None, None)
            len_str = self.sd.read(4)
            msg_len = int(struct.unpack("!L", len_str)[0])
            msg = ""
            while len(msg) != msg_len:
                data = self.sd.read(min(2048, msg_len - len(msg)))
                if not len(data):
                    break
                msg += data
            if len(msg) != msg_len:
                return(None, None)
        except KeyboardInterrupt:
            raise
        return (msg_type, msg)
    
    def close(self):
        self.s.close()
        self.s = None
        self.sd = None