import socket
import _thread
import sys

from .proxyserver import proxyserve

class parseconndata:
    def __init__(self, data, conn, addr):
        try:
            line = data.split('\n')[0]
            url = line.split(' ')[1]

            host_pos = url.find('://')
            if(host_pos == -1):
                temp_url = url
            else:
                temp_url = url[(host_pos+3):]

            port_pos = temp_url.find(':')
            
            web_pos = temp_url.find('/')
            if(web_pos == -1):
                web_pos = len(temp_url)
            port = -1
            if(port_pos == -1 or web_pos < port_pos):
                port = 80
                webserver = temp_url[:web_pos]
            else:
                port = int((temp_url[(port_pos+1):])[web_pos-port_pos+1])
                webserver = temp[:port_pos]
            self.webserver, self.port, self.conn, self.addr, self.data = webserver, port, conn, addr, data
        except Exception as e:
            print("Exit when parsing given url")


class connection:
    def __init__(self, config):
        self.config = config
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.config['hostname'], self.config['portname']))

            self.serverSocket.listen(10)
            self._clients = {}
            print("Socket Initialized")
            self.initializeconnection()
        except Exception as e:
            print("Unable to initialized the Socket")
            print(e)
            sys.exit(2)
    
    def initializeconnection(self):
        while True:
            try:
                self.conn, self.addr = self.serverSocket.accept()
                data = self.conn.recv(self.config['buffer_size'])
                self.newthread(data, self.conn, self.addr)
            except KeyboardInterrupt as e:
                self.shutdown()
        self.serverSocket.close()

    def newthread(self, *args):
        try:
            _thread.start_new_thread(self.makeconnection, *args)
        except Exception as e:
            print("Connection closed starting new thread",e)
            self.shutdown()

    def makeconnection(self, *args):
        k = parseconndata()
        self.proxy = proxyserve()
        for i in self.proxy.createProxyServer(k.webserver, k.port, k.conn, k.data, k.addr):
            self.conn.send(i)

    def shutdown(self):
        self.serverSocket.close()
        print("Connection Closed")
        sys.exit(1)
