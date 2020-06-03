import socket
import sys

class proxyserve:
    def __init__(self):
        self.serverSocket = ''
        self.buffer_size = 4096
    
    def createProxyServer(self, webserver, port, conn, data, addr):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.connect((webserver, port))
            self.serverSocket.send(data)

            while True:
                reply = self.serverSocket.recv(self.buffer_size)
                if(len(reply) > 0):
                    yield reply
                else:
                    break
            self.serverSocket.close()
        except Exception as e:
            self.serverSocket.close()
            sys.exit(1)
