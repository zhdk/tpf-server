import socket
import sys

# init values
cdef str UDP_IP = '0.0.0.0'
cdef int DEFAULT_UDP_PORT = 4460
LINK_LOOKUP = dict()
TOKEN_LOOKUP = dict()

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

cdef void  addtoken(str token, str ipaddr, int port):
    "Remember token for given address or if token has been used already, create a link"
    if token in TOKEN_LOOKUP:
        if (ipaddr, port) not in TOKEN_LOOKUP[token]:
            TOKEN_LOOKUP[token].append((ipaddr, port))
            LINK_LOOKUP[TOKEN_LOOKUP[token][0]] = TOKEN_LOOKUP[token][1]
            LINK_LOOKUP[TOKEN_LOOKUP[token][1]] = TOKEN_LOOKUP[token][0]
            del TOKEN_LOOKUP[token]
    else:
        TOKEN_LOOKUP[token] = [(ipaddr, port)]

cdef void clear():
    "Clear token  and link cache"
    LINK_LOOKUP.clear()
    TOKEN_LOOKUP.clear()

cpdef void main():
    "Main loop listening for incoming packets"
    cdef str ipaddr = 'xxx.xxx.xxx.xxx'
    cdef int port = 65536
    srcaddr = (ipaddr, port)
    destaddr = (ipaddr, port)
    cdef str token
    try:
        while True:
            data, srcaddr = SOCK.recvfrom(65507)

            # check token
            if data[0:7] == b'_TOKEN ':
                token = data.decode().split()[1]
                addtoken(token, srcaddr[0], srcaddr[1])

            # forward data according to lookup table
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
