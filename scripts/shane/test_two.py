#!/usr/bin/env python

import socket


def main():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.settimeout(5)
    try:
        tcp_sock.connect(('localhost', 4156))
        tcp_sock.send('hello')
        data = tcp_sock.recv(1024)
        print data
    except socket.timeout, e:
        pass

if __name__ == '__main__':
    main()
