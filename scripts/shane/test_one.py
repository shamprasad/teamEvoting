#!/usr/bin/env python

import socket
import cPickle as pickle
import time
from threading import Thread


def client_handler(peers, tcp_client_sock):
    data = tcp_client_sock.recv(1024)
    peers.append(data)
    print peers
    print time.time()
    tcp_client_sock.send('hello')

def main():
    peers = []
    tcp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_sock.settimeout(5)
    tcp_server_sock.bind(('localhost', 4156))
    tcp_server_sock.listen(5)

    while True:
        try:
            tcp_client_sock, client_addr = tcp_server_sock.accept()
            Thread(target=client_handler, args=(peers,
                                                tcp_client_sock)).start()
        except socket.timeout, e:
            pass

if __name__ == '__main__':
    main()
