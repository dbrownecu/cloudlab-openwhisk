import socket
import ssl
import time

SERVERPEM = "keys/server.crt"
PRIVATEKEY = "keys/server.key"

MAXBUFSIZE = 8192


def listener():
    buff = []
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(SERVERPEM, PRIVATEKEY)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((socket.gethostname(), 8443))
        sock.listen(10)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            print("connection {}\n".format(conn))
            print("address {}\n".format(addr))
            data = conn.recv(MAXBUFSIZE).decode('utf-8')
            while data:
                print("{},received,{}, len {}".format(time.time(), data, len(data)))
                data = conn.recv(MAXBUFSIZE).decode('utf-8')


if __name__ == '__main__':
    while True:
        listener()
        print("Connection ended listening again")
