#!/usr/bin/env python3

import socket
import sys

# init values
UDP_IP = '0.0.0.0'
DEFAULT_UDP_PORT = 4460
linklookup = dict()
tokenlookup = dict()

try:
    UDP_PORT = int(sys.argv[1])
except ValueError:
    sys.stderr.write("[ERROR] Specified port is not a number\n")
    sys.exit(1)
except IndexError:
    UDP_PORT = DEFAULT_UDP_PORT

try:
    assert(1024 <= UDP_PORT <= 65535)
except AssertionError:
    sys.stderr.write("[ERROR] Specified port '%s' is out of valid range (1024-65535).\n" % UDP_PORT)
    sys.exit(1)

# create a socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
except socket.error(msg):
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

def addtoken(token, addr):
    if token in tokenlookup:
        if addr not in tokenlookup[token]:
            tokenlookup[token].append(addr)
            linklookup[tokenlookup[token][0]] = tokenlookup[token][1]
            linklookup[tokenlookup[token][1]] = tokenlookup[token][0]
            del tokenlookup[token]
    else:
        tokenlookup[token] = [addr]

def clear():
    linklookup.clear()
    tokenlookup.clear()

# our main loop
def main():
    srcaddr = None
    try:
        while True:
            data, srcaddr = sock.recvfrom(65507)

            # check token
            if data[0:7] == b'_TOKEN ':
                token = data.split()
                try:
                    addtoken(token[1], srcaddr)
                except:
                    pass

            # forward data according to lookup table
            else:
                try:
                    destaddr = linklookup[srcaddr]
                    sock.sendto(data, destaddr)
                except:
                    pass
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()

