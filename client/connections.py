from __future__ import print_function
import sys
import os
import mimetypes
sys.path.insert(0, '..')
from context import bluelet
from .proxyserver import AsyncHTTPClient
import json
from context.log import log_connect, log_info, log_warning, log_error
from context import optionparser

Port = 8000
RPort = 8091
RHost = ''

def parserargs():
    global Port
    global RPort
    global RHost
    args = optionparser.client()
    if(args.port):
        Port = args.port
    if(args.rport):
        RPort = args.rport
    if(args.rhost):
        RHost = args.rhost

def parse_request(lines):
    """Parse an HTTP request."""
    method, path, version = lines.pop(0).split(None, 2)
    headers = []
    for line in lines:
        if not line:
            continue
        # key, value = line.split(b': ', 1)
        headers.append(line.decode('utf-8'))
    return method, path, headers


def respond(method, path, headers):
    data = AsyncHTTPClient.fetch(path,headers,method,RHost,RPort)
    return data

def webrequest(conn):
    """A Bluelet coroutine implementing an HTTP server."""
    # Get the HTTP request.
    request = []
    while True:
        line = (yield conn.readline(b'\r\n')).strip()
        if not line:
            # End of headers.
            break
        request.append(line)
    

    # Make sure a request was sent.
    if not request:
        return
    
    # Parse and log the request and get the response values.
    method, path, headers = parse_request(request)
    log_connect(method.decode('utf-8'), path.decode('utf-8'))
    response = respond(method, path, headers)
    # Send response.
    yield conn.sendall(response)
    # for key, value in headers.items():
    #     yield conn.sendall(("%s: %s\r\n" % (key, value)).encode('utf8'))
    # yield conn.sendall(b"\r\n")
    # yield conn.sendall(content)

def connectclient():
    if len(sys.argv) > 1:
        parserargs()
        Rstring = "Remote Server "+RHost + ":" + str(RPort)
        log_info(Rstring)
    if(not RHost):
        log_error("No Remote Address")
        sys.exit(2)
    log_info("Starting Client")
    log_info('http://127.0.0.1:'+str(Port)+'/')
    bluelet.run(bluelet.server('', Port, webrequest))
