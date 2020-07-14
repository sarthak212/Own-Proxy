import argparse

def client():
    parser = argparse.ArgumentParser(description='OwnProxy Client')
    parser.add_argument('--port',type=int,help="Port on which your client server is listening")
    parser.add_argument('--rport',type=int,help="Port on which your Remote Server is listening")
    parser.add_argument('--rhost',help="Ip address in which your remote server is running")
    args = parser.parse_args()
    return args

def server():
    parser = argparse.ArgumentParser(description='OwnProxy Server')
    parser.add_argument('--port',type=int,help="Port on which your server is listening")
    args = parser.parse_args()
    return args