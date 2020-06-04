import socket
import sys

class proxyserve:
    def __init__(self):
        self.serverSocket = ''
        self.buffer_size = 4096
    
    def createProxyServer(self, webserver, port, conn, data, addr):
        try:
            host = socket.gethostbyname(webserver)
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.connect((host, port))
            self.serverSocket.sendall(data)

            while True:
                reply = self.serverSocket.recv(self.buffer_size)
                if(len(reply) > 0):
                    yield reply
                else:
                    break
            self.serverSocket.close()
        except Exception as e:
            sys.exit(1)
