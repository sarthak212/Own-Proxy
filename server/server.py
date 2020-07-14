
from urllib.parse import urlparse
from urllib.request import urlopen
import socket

class AsyncHTTPClient(object):
    """A basic Bluelet-based asynchronous HTTP client. Only supports
    very simple GET queries.
    """
    def __init__(self, host, port, path, headers, method):
        self.host = host
        self.hostname = socket.gethostbyname(self.host)
        self.port = port
        self.path = path.decode('utf-8')
        self.header = headers
        self.method = method.decode('utf-8')

    def headers(self):
        """Returns the HTTP headers for this request."""
        heads = [
            "%s %s HTTP/1.1" % (self.method,self.path)
        ]
        heads.extend(self.header)
        return "\r\n".join(heads).encode('utf8') + b"\r\n\r\n"


    # Convenience methods.

    @classmethod
    def from_url(cls, url, header, method):
        """Construct a request for the specified URL."""
        res = urlparse(url)
        path = res.path
        if res.query:
            path += b'?' + res.query
        hostname = header[0].split(': ')[1]
        return cls(hostname, res.port or 80, path, header, method)

    @classmethod
    def fetch(cls, url, header, method):
        """Fetch content from an HTTP URL. This is a coroutine suitable
        for yielding to bluelet.
        """
        client = cls.from_url(url, header, method)
        client._connect()
        client._request()
        return client._read()
    

    # Internal coroutines.

    def _connect(self):
        self.sock = socket.create_connection((self.hostname, self.port))

    def _request(self):
        self.sock.sendall(self.headers())

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