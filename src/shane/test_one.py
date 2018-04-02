import socket
from random import randint


def main():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.settimeout(5)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind(('localhost', randint(50000, 60000)))
    tcp_addr = tcp_sock.getsockname()
    print tcp_addr

if __name__ == '__main__':
    main()
