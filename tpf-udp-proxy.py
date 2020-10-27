#!/usr/bin/env python3
#
# udp_dyn_proxy manages an internal lookup table to relay incoming
# udp datagrams to a certain destination
#
# The lookup tables contains pairs of ip:port tuples. The table
# can be edited by sending UDP datagrams from localhost.
#
# EXAPMLES
#
# Add link:
#
#   addlink 10.158.0.53 12304 8.8.8.8 45682
#
# Delete link:
#
#   dellink 10.158.0.53 12304 8.8.8.8 45682
#
# Print lookup table:
#
#   printlinks
#

import socket
import sys

# init values
UDP_IP = '0.0.0.0'
linklookup = dict()
tokenlookup = dict()
DEFAULT_UDP_PORT = 4460
srcaddr = None

try:
    UDP_PORT = int(sys.argv[1])
except ValueError:
    print("Specified port is not a number")
    sys.exit(1)
except IndexError:
    UDP_PORT = DEFAULT_UDP_PORT

# haben wir einen gueltigen Port
if not isinstance( UDP_PORT, int ) or not  1024 <= UDP_PORT <= 65535:
    print("WSpecified port (", UDP_PORT, ") is invalid.")
    print("Valid port range: 1024 - 65535")
    sys.exit(1)

# create a socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
except socket.error(msg):
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

# lookup table manipulation methods
def addlink():
    try:
        ip1, port1, ip2, port2 = command[1:]
        port1 = int(port1)
        port2 = int(port2)
        assert 32768 <= port1 <= 65535
        assert 32768 <= port2 <= 65535
        socket.inet_aton(ip1)
        socket.inet_aton(ip2)
        linklookup[(ip1, port1)] = (ip2, port2)
        linklookup[(ip2, port2)] = (ip1, port1)
    except:
        payload = "Error while executing: " + " ".join(command) + '\n'
        sock.sendto(payload.encode(), srcaddr)

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
    try:
        linklookup.clear()
        tokenlookup.clear()
    except:
        payload = "Clearing linklookup table failed\n"
        sock.sendto(payload.encode(), srcaddr)

def dellink():
    try:
        ip1, port1, ip2, port2 = command[1:]
        del linklookup[(ip1, int(port1))]
        del linklookup[(ip2, int(port2))]
    except:
        payload = "Error while executing: " + " ".join(command) + '\n'
        sock.sendto(payload.encode(), srcaddr)

def printlinks():
    sock.sendto('LINK LOOKUP TABLE\n'.encode(), srcaddr)
    for lookup_key, lookup_value in linklookup.items():
        payload = lookup_key[0] + ':' + str(lookup_key[1]) + ' => ' + \
                  lookup_value[0] + ':' + str(lookup_value[1]) + '\n'
        sock.sendto(payload.encode(), srcaddr)

# map command to method calls
methods = {
    'addlink': addlink,
    'clear': clear,
    'dellink': dellink,
    'printlinks': printlinks,
    }

# our main loop
def main():
    global srcaddr
    try:
        while True:
            data, srcaddr = sock.recvfrom(65507)
            try:
                data_serialized = data.decode()
            except UnicodeDecodeError:
                data_serialized = ''

            # manipulate table if packet is from localhost
            if srcaddr[0] == '127.0.0.1':
                command = data_serialized.split()
                try:
                    methods[command[0]]()
                except KeyError:
                    payload = command[0] + ': method not implemented\n'
                    sock.sendto(payload.encode(), srcaddr)

            # check token
            elif data_serialized[0:7] == '_TOKEN ':
                token = data_serialized.split()
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

