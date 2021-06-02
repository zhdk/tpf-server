#!/usr/bin/env python3
"""
This script is part of tpf-server. It relays UDP packets between clients.
Connections are established by clients sending token messages. If two clients
send the same token message, subsequent packets are relayed between those
clients.
"""

import socket
import sys
import time

# init values
UDP_IP = '0.0.0.0'
DEFAULT_UDP_PORT = 4460
LINK_LOOKUP = dict()
TOKEN_LOOKUP = dict()
PURGE_TIMEOUT = 10

try:
    UDP_PORT = int(sys.argv[1])
except ValueError:
    sys.stderr.write("[ERROR] Specified port is not a number\n")
    sys.exit(1)
except IndexError:
    UDP_PORT = DEFAULT_UDP_PORT

try:
    assert 1024 <= UDP_PORT <= 65535
except AssertionError:
    sys.stderr.write("[ERROR] Specified port '%s' is out of valid range (1024-65535).\n" % UDP_PORT)
    sys.exit(1)

# create a socket
try:
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCK.bind((UDP_IP, UDP_PORT))
except socket.error as error:
    sys.stderr.write("[ERROR] %s\n" % error)
    sys.exit(1)

def addtoken(token, addr):
    "Remember token for given address or if token has been used already, create a link"
    if token in TOKEN_LOOKUP:
        if addr not in TOKEN_LOOKUP[token]:
            TOKEN_LOOKUP[token].append(addr)
            LINK_LOOKUP[TOKEN_LOOKUP[token][0]] = TOKEN_LOOKUP[token][1]
            LINK_LOOKUP[TOKEN_LOOKUP[token][1]] = TOKEN_LOOKUP[token][0]
            del TOKEN_LOOKUP[token]
    else:
        TOKEN_LOOKUP[token] = [addr]

def printlinks(srcaddr):
    "Print lookups in human-readable form to requesting party"
    SOCK.sendto(b'-- LINKS ----------------------------\n', srcaddr)
    for fromaddr in LINK_LOOKUP.keys():
        toaddr = LINK_LOOKUP[fromaddr]
        line = f'{fromaddr[0]}:{fromaddr[1]} => {toaddr[0]}:{toaddr[1]}\n'
        SOCK.sendto(line.encode(), srcaddr)
    SOCK.sendto(b'-- TOKENS ---------------------------\n', srcaddr)
    for token in TOKEN_LOOKUP.keys():
        addr = TOKEN_LOOKUP[token][0]
        line = f'{token.decode()}: {addr[0]}:{addr[1]}\n'
        SOCK.sendto(line.encode(), srcaddr)

def clear():
    "Clear token  and link cache"
    LINK_LOOKUP.clear()
    TOKEN_LOOKUP.clear()

def main():
    "Main loop listening for incoming packets and relaying them"
    prev_ts = time.time()
    try:
        while True:
            data, srcaddr = SOCK.recvfrom(65507)
            current_ts = time.time()
            if (prev_ts + PURGE_TIMEOUT) < current_ts:
                clear()
            prev_ts = current_ts
            if data[0:7] == b'_TOKEN ':
                token = data.split()
                addtoken(token[1], srcaddr)
            elif data == b'_CHECK\n':
                printlinks(srcaddr)
            else:
                try:
                    destaddr = LINK_LOOKUP[srcaddr]
                    SOCK.sendto(data, destaddr)
                except KeyError:
                    pass
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
