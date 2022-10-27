import socket
import ssl
import time
import json
CERTSTRING="""-----BEGIN CERTIFICATE-----
MIIDzzCCArcCFECe1578Mv9NE/jw7ypS5TaJ0aUlMA0GCSqGSIb3DQEBCwUAMIGj
MQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2Fu
IEZyYW5jaXNjbzETMBEGA1UECgwKQ1UgQm91bGRlcjEUMBIGA1UECwwLU3lzdGVt
cyBMYWIxETAPBgNVBAMMCHNlcnZlcmNhMSkwJwYJKoZIhvcNAQkBFhpkd2lnaHQu
YnJvd25lQGNvbG9yYWRvLmVkdTAeFw0yMjEwMjYyMzQ3MzRaFw0zMjEwMjMyMzQ3
MzRaMIGjMQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UE
BwwNU2FuIEZyYW5jaXNjbzETMBEGA1UECgwKQ1UgQm91bGRlcjEUMBIGA1UECwwL
U3lzdGVtcyBMYWIxETAPBgNVBAMMCGNsaWVudGNhMSkwJwYJKoZIhvcNAQkBFhpk
d2lnaHQuYnJvd25lQGNvbG9yYWRvLmVkdTCCASIwDQYJKoZIhvcNAQEBBQADggEP
ADCCAQoCggEBAJ5994NoTtzqApd3hRuAUh1xP1k6cxaKvHvzskjiF9PDeDqSzyDJ
3GcvSUgXBxHL0oaFqLIa3TwYqFDRF5d9oEOvoqvE1FE4/hundYrx/Mz+sWcitMRf
wR/CPoW7X5cE2lImMzB3kfstwvRM1IbfnSzvn9tk7uFGjekWNMht1mIzjwcvFqpW
SVAXUrWARCJVcvcvzCxp3j2r/h0buRYZGlJfJ5Gy+HY3UD7W/5bHaIjCbqJwWSqL
cAvsOyR0FglF2xttscAJgjuwKCNOojyCpP0nWroDTohlnhpJowrqvBcfHE3BTRRj
UpyeB5ajRJLgAHDzDqqIxdquGtA42YAyIOMCAwEAATANBgkqhkiG9w0BAQsFAAOC
AQEAgwxD7GRd2JBGZcWodAMKLO3mVHc4WyXEou4EyLcF2nHXwJ7lGsdlPhnTPdKg
kA12ZuN2JD46UWMHIg2Sk1tbo1G2aJfsRiwGr1V51HLmZEj+QFVuWnkzIzFDQcgL
20I46LrKexgaE7J96wPAfq3750FUrZ/QYIVZDPN9oKkie7OqC+Ho1JALl/T2qL7C
k6k300LbV+NWkyE16flZao65rFPI0HVJcFKGJrDyA5ye7HrzK6jKOnSA0Fs+c7o3
IoMnxDduVLkhnuwCbSsPFPxNaCacju2fxW2yIvU5y/CNggpNeJQlNzfDRV7wzidi
EZZdP4LbqUQ38Npik2SJtj4iSA==
-----END CERTIFICATE-----"""


KEYSTRING="""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCeffeDaE7c6gKX
d4UbgFIdcT9ZOnMWirx787JI4hfTw3g6ks8gydxnL0lIFwcRy9KGhaiyGt08GKhQ
0ReXfaBDr6KrxNRROP4bp3WK8fzM/rFnIrTEX8Efwj6Fu1+XBNpSJjMwd5H7LcL0
TNSG350s75/bZO7hRo3pFjTIbdZiM48HLxaqVklQF1K1gEQiVXL3L8wsad49q/4d
G7kWGRpSXyeRsvh2N1A+1v+Wx2iIwm6icFkqi3AL7DskdBYJRdsbbbHACYI7sCgj
TqI8gqT9J1q6A06IZZ4aSaMK6rwXHxxNwU0UY1KcngeWo0SS4ABw8w6qiMXarhrQ
ONmAMiDjAgMBAAECggEAO48y2Fr2Z+Y4mxr7Fl6efRn1qF5iqXHxatMliGYOdjHa
mIha9gNlpBENBN5CddmWf57yyht2UAMkHVq19uPqugTiqJILB4rXUyUW8uQFEDQW
Dp/oNnOVa43fWPoU7feQ45YfXnNQlIeZ35yPsS+PLTfPZu8DJf0RjyodI8TC75vA
v7THTdeMmuhf+Ivx9yiTvOfjuFHvc7A6NDNJpOgF+rbULNXnxIci5ttdDK7uGzpF
Wvk3Ha9SI474ewa83z0vhqbcNFUfncicwVMtdoCFHcm9Qb4d8IBrd0P/uug2wncs
hs0ER9iw4bXamjcC35ucxoh9snqRhq2K07srS2Z2gQKBgQDXyjnNAPGQe060bmmS
2CIXRvW3nWv75X0w3i0ogH0nyt53ezWlbDsaiMEQIZovvoB0bT34sO7tFHj9YYSk
B6mWK2eCKZmjx//LRrdoBGuNBkoJLCZ8DB0IBVf4fEK7qX6O/bFC4BIVIgEo72Le
fIce36gM7e3bksY+y/BNYIp4kQKBgQC8BnlkvmcRCR79JpMx0aM3X/E6WfYxyNKk
yQpx5bbG98xfYxjyd85QF9BKw5giG3T9Ba/sO4JRn9UTVJf2/vg2baZxKmbYzv5L
4J/jbUpSkPeQjR7k4KvrB8TlfFIVMJHNUspyWZpz4WiPfJ3bOpP14JIFUr43JZzr
Q0vCUMhcMwKBgQCebBb3TIQMYJqtmInlhsuwbyYiQW5vplG8uMBKhdpchnHBIjGG
WukhV9j1cNXzy1YfI7xlgfBHGcqhqyBoFEAKwZ7iTow/U6uVnzszIFudU0qzZThz
xajipJmrEf8kKxGBBPtIb5yW6zoSxXy+fonsvqJvq5X+p8jnfW3UQNYoIQKBgH3T
U09gv7Y9xVghhWVUZgY7lUG4TDHas2QFCZFY6WzTDRhUR7CTDiS5GvG9XMSOXUap
lKXg2P/olv29oYhv7gj2bejTOEokkzaR1k2qqI8CZjl8xszhsQqyg0gTXxbBDwE5
QzMs1Vhw4rkK6tR3qeZj5zPawGJFMHKb8UnTJ5HTAoGBAMdc0sAcy6x4G/cj7F+b
0bDg9MaWD168pjuYWkl6sXsRfJiy9OE3h6lOW028s/UW8rv2dTsuodX41/hQQ0Ey
aRmPrkWzdVInXsZNgxSm+TTQHNwT+2uflvsUe92/0fOfJo09V18y3yOqt3Iby/lc
LHL1JBlpleFmBK6ZZ72jRilx
-----END PRIVATE KEY-----"""

KEYFILE ="/tmp/clientKey"
CERTFILE = "/tmp/clientCert"

def genFiles():
    fn = open(KEYFILE,"w")
    fn.write(KEYSTRING)
    fn.close()
    fn = open(CERTFILE,"w")
    fn.write(CERTSTRING)
    fn.close()



def connectSendLoop(host, interval, delay ):

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("Needcabundle.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:

            for i in range(interval):
                t = time.time()
                stamp = "{}: {} this is a test\n".format(i, t)
                ssock.send(stamp.encode("utf-8"))
                time.sleep(delay)


def commonfunc(host,interval,delay):
    connectSendLoop(host,interval,delay)
    return {
        "statusCode" :0,
        "body": json.dumps(({
            "label": "This is empty",
        })),
    }



def main(args):
    host = args.get("host","localhost")
    interval = args.get("interval",10)
    delay = args.get("delay",0)

    retval = commonfunc(host,interval, delay)
    return retval


if __name__ == '__main__':
    host = "localhost"
    interval = 100
    delay = 0

    retval = commonfunc(host,interval, delay)
