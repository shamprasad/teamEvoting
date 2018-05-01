#!/usr/bin/env python

import socket
import cPickle as pickle
from time import time
from threading import Thread, Lock


SERVER_ADDRESS = ('localhost', 4156)
HEARTBEAT_TIMER = 30
PEERS_LOCK = Lock()

# Method for handling client requests
def client_handler(peers, tcp_client_sock):
    # If client sends data
    try:
        data = tcp_client_sock.recv(1024)
        data = pickle.loads(data)
        # If client requests peers
        # then send all address of known active peers
        if data[0] == "request peers":
            PEERS_LOCK.acquire()
            if data[1] not in peers['address']:
                peers['address'].append(data[1])
                peers['timer'].append(time())
            else:
                index = peers['address'].index(data[1])
                peers['timer'][index] = time()
            msg = pickle.dumps(peers['address'])
            PEERS_LOCK.release()
            tcp_client_sock.send(msg)
    # If client doesn't sent anything, assume inactive and remove peer
    except (socket.timeout, socket.error), e:
        PEERS_LOCK.acquire()
        index = peers['address'].index(peer)
        del peers['address'][index]
        del peers['timer'][index]
        PEERS_LOCK.release()
    # Shutdown and close tcp socket
    tcp_client_sock.close()

# Main method
def main():
    # Data structure for saving active peers
    peers = {'address': [], 'timer': []}
    # Initialize server tcp socket
    server_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_tcp_sock.settimeout(5)
    server_tcp_sock.bind(SERVER_ADDRESS)
    server_tcp_sock.listen(5)
    # Iterate indefinitely
    while True:
        # If client requests to connect
        # then handle request
        try:
            tcp_client_sock, client_addr = server_tcp_sock.accept()
            Thread(target=client_handler,
                   args=(peers,
                         tcp_client_sock)).start()
        # If no clients request to connect
        # then do nothing
        except socket.timeout, e:
            pass
        # Delete inactive peers
        for address, timer in zip(peers['address'], peers['timer']):
            if timer+HEARTBEAT_TIMER <= time():
                index = peers['address'].index(address)
                del peers['address'][index]
                del peers['timer'][index]
        print peers['address']

# Method for handling direct script calls
if __name__ == '__main__':
    main()
