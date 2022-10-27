import socket
import ssl

SERVERPEM="keys/server.crt"
PRIVATEKEY="keys/server.key"
def listener():
    buff = []
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(SERVERPEM,PRIVATEKEY)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('127.0.0.1',8443))
        sock.listen(10)
        with context.wrap_socket(sock,server_side=True) as ssock:
            conn, addr = ssock.accept()
            print("connection {}\n".format(conn))
            print("address {}\n".format(addr))
            while True:
                data = ssock.recv(1024)
                if not data:
                    break
                print("received: {}".format(data.decode('utf-8')))


if __name__ == '__main__':
    listener()