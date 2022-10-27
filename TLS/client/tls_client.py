import socket
import ssl
import time
import json
import os
CLIENTCERT="""-----BEGIN CERTIFICATE-----
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




CERTFILE = "/tmp/clientCert"

def genFiles():
    fn = open(CERTFILE,"w")
    fn.write(CLIENTCERT)
    fn.close()
    os.chmod(CERTFILE, 0o700)


def connectSendLoop(host, port, interval, delay ):

    genFiles()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERTFILE)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection(('127.0.0.1', port)) as  sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            if ssock:
                print("soket {}".format(ssock))
                for i in range(interval):
                    t = time.time()
                    stamp = "{}: {} this is a test\n".format(i, t)
                    print(stamp)
                    ssock.send(stamp.encode("utf-8"))
                    time.sleep(delay)
            else:
                print("Socket problems {}\n".format(ssock))

def commonfunc(host,port,interval,delay):
    connectSendLoop(host,port, interval,delay)
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

    retval = commonfunc(host,port, interval, delay)
    return retval


if __name__ == '__main__':
    host = "localhost"
    port = 8443
    interval = 100
    delay = 0

    retval = commonfunc(host,port,interval, delay)
