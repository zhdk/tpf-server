## tpf-server

NOTE: tpf-server is still in an experimental state and does not guarantuee
      backwards compatibility yet.


### About

**[tpf-server](https://gitlab.zhdk.ch/TPF/tpf-server)** is used to connect instances
of tpf-clients. It is supposed to run on server with a public IP address.

**[tpf-client](https://gitlab.zhdk.ch/TPF/tpf-client)** is a low-latency audio
transmission software based on the jacktrip protocol and built in Pure Data.


For more information visit:

  * https://gitlab.zhdk.ch/TPF/tpf-server
  * https://gitlab.zhdk.ch/TPF/tpf-client


### Installation

Install Pure Data with your package manager or get binaries
from:

  https://puredata.info/downloads/

You need the following externals to run tpf-client

  * iemnet
  * osc
  * slip

You can install externals through the Pd menu:
'Help' -> 'Find Externals'

tpf-server uses netpd-server as a git submodule, thus make
sure to clone the repository like this:

```
git clone --recursive https://gitlab.zhdk.ch/TPF/tpf-server
```

### Run tpf-server

For the server to be reachable by the clients, it should run on
a machine with a public IP address. On a head-less machine, you
probably want to run it in nogui mode:

```
pd -nogui -open tpf-server/tpf-server.pd
```

The server opens a listening socket on TCP-port 3025. So make
sure that this port is open in your firewall configuration.
The TCP-Port 3025 is only used for client communication and not for
audio transmission. The audio transmission is using UDP-Port 4460
and requires a separate Python script to be running:

```
./tpf-udp-proxy.py
```

This waits for incoming client connections and relays UDP packets
between clients.

### Issues

For any bug, issue or suggestion, please open an issue [here](https://github.com/reduzent/tpf-server/issues).

### Authors

  * Roman Haefeli <roman.haefeli@zhdk.ch>
  * Johannes Schütt <johannes.schuett@zhdk.ch>

### License

  GPL 3.0 (see LICENSE.txt)

