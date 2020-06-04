import socket
import threading
import sys

from .proxyserver import proxyserve

def threadconnection(connection, *args):
    parse_data = parseconndata(*args)
    connection.proxy = proxyserve()
    for i in connection.proxy.createProxyServer(parse_data.webserver, parse_data.port, parse_data.conn, parse_data.data, parse_data.addr):
        connection.conn.send(i)

class parseconndata:
    def __init__(self, data, conn, addr):
        try:
            encode_data = data
            data = data.decode('utf-8')
            url = data.split(' ')[1]

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
            self.webserver, self.port, self.conn, self.addr, self.data = webserver, port, conn, addr, encode_data
        except Exception as e:
            print("Exit when parsing given url")
            print(e)
            print("Error on line ".format(sys.exc_info()[-1].tb_lineno))
            sys.exit(2)


class connection:
    def __init__(self, config):
        self.config = config
        self.thread = []
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.config['hostname'], self.config['portname']))

            self.serverSocket.listen()
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
        list2 = []
        for i in args:
            list2.append(i)
        list1 = tuple([self] + list2)
        try:
            k = threading.Thread(target = threadconnection, args = list1)
            k.start()
            self.thread.append(k)
        except Exception as e:
            print("Connection closed starting new thread",e)
            self.shutdown()

    def shutdown(self):
        self.serverSocket.close()
        print("Connection Closed")
        sys.exit(1)
