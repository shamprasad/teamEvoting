#!/usr/bin/env python

import socket
import cPickle as pickle
import time
from threading import Thread


def client_handler(peers, tcp_client_sock):
    try:
        data = tcp_client_sock.recv(1024)
        data = pickle.loads(data)
        if data[0] == "request peers":
            if data[1] not in peers:
                peers.append(data[1])
            msg = pickle.dumps(peers)
            tcp_client_sock.send(msg)
        tcp_client_sock.shutdown(socket.SHUT_RDWR)
        tcp_client_sock.close()
    except (socket.timeout, socket.error), e:
        peers.remove(peer)

def verify_peers(peers):
    for peer in peers[:]:
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.settimeout(5)
        try:
            tcp_sock.connect(peer)
            tcp_sock.send('hello peer')
            data = tcp_sock.recv(1024)
            tcp_sock.shutdown(socket.SHUT_RDWR)
            tcp_sock.close()
        except (socket.timeout, socket.error), e:
            peers.remove(peer)

def main():
    peers = []
    tcp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_sock.settimeout(5)
    tcp_server_sock.bind(('localhost', 4156))
    tcp_server_sock.listen(5)

    timer = time.time()

    while True:
        try:
            tcp_client_sock, client_addr = tcp_server_sock.accept()
            Thread(target=client_handler, args=(peers,
                                                tcp_client_sock)).start()
        except socket.timeout, e:
            pass

        if timer+5 <= time.time():
            timer += 5
            Thread(target=verify_peers, args=(peers,)).start()
        print peers


if __name__ == '__main__':
    main()
