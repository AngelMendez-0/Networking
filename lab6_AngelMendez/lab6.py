# author: Angel Mendez

from urllib.parse import urlparse
from random import randint
from scapy.all import *
from socket import gethostbyname
from sys import argv

def main():
    if len(argv) != 2:
        return

    url = argv[1]
    if not url.startswith("http://"):
        url = "http://" + url

    parsed = urlparse(url)

    host = parsed.hostname
    path = parsed.path if parsed.path != "" else "/"
    port = 80

    dst_ip = gethostbyname(host)
    src_port = randint(1024, 65535)

    seq = len("Angel")

    ip = IP(dst = dst_ip)

    syn = TCP(sport = src_port, dport = port, flags = "S", seq = seq)
    synAck = sr1(ip / syn, timeout = 3, verbose = 0)

    if synAck is None:
        return

    ackSeq = seq + 1
    ackAck = synAck.seq + 1

    ackPkt = TCP(
        sport = src_port,
        dport = port,
        flags = "A",
        seq = ackSeq,
        ack = ackAck
    )

    send(ip / ackPkt, verbose = 0)

    httpGet = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    getPkt = TCP(
        sport = src_port,
        dport = port,
        flags = "PA",
        seq = ackSeq,
        ack = ackAck
    )

    send(ip / getPkt / Raw(load = httpGet), verbose = 0)

if __name__ == "__main__":
    main()
