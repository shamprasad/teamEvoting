import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 4156))
    sock.listen(1)
    conn, addr = sock.accept()
    data = conn.recv(1024)
    print addr
    print data
    conn.send('good-bye world')

if __name__ == '__main__':
    main()
