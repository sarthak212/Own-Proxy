
from urllib.parse import urlparse
from urllib.request import urlopen
import socket
from context.log import log_info, log_error,log_warning
from context import encrypt

class AsyncHTTPClient(object):
    """A basic Bluelet-based asynchronous HTTP client. Only supports
    very simple GET queries.
    """
    def __init__(self, host, port, path, headers, method,Rhost,Rport):
        self.host = host.decode('utf-8')
        self.hostname = socket.gethostbyname(self.host)
        self.port = port
        self.path = path.decode('utf-8')
        self.header = headers
        self.method = method.decode('utf-8')
        self.rhost = Rhost
        self.rport = Rport

    def headers(self):
        """Returns the HTTP headers for this request."""
        heads = [
            "%s %s HTTP/1.1" % (self.method,self.path)
        ]
        heads.extend(self.header)
        return "\r\n".join(heads).encode('utf8') + b"\r\n\r\n"


    # Convenience methods.

    @classmethod
    def from_url(cls, url, header, method,rhost,rport):
        """Construct a request for the specified URL."""
        res = urlparse(url)
        path = res.path
        if res.query:
            path += b'?' + res.query
        return cls(res.hostname, res.port or 80, path, header, method,rhost,rport)

    @classmethod
    def fetch(cls, url, header, method,rhost,rport):
        """Fetch content from an HTTP URL. This is a coroutine suitable
        for yielding to bluelet.
        """
        client = cls.from_url(url, header, method,rhost,rport)
        client._connect()
        client._request()
        return client._read()
    

    # Internal coroutines.

    def _connect(self):
        self.sock = socket.create_connection((self.rhost, self.rport))

    def _request(self):
        self.sock.sendall(encrypt.encrypt(self.headers()))

    def _read(self):
        buf = []
        res = b''
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            buf.append(data)
            res += data
        return res