## tpf-server

NOTE: tpf-server is still in an experimental state and does not guarantuee
      backwards compatibility yet.


### About

**[tpf-server](https://github.com/zhdk/tpf-server)** is used to connect instances
of tpf-clients. It is supposed to run a on server with a public IP address.

**[tpf-client](https://github.com/zhdk/tpf-client)** is a low-latency audio
transmission software based on the [AoO](https://git.iem.at/cm/aoo)  (Audio-over-OSC)
protocol and built in Pure Data.


For more information visit:

  * https://github.com/zhdk/tpf-server
  * https://github.com/zhdk/tpf-client


### Installation

NOTE: Find detailed instructions in [here](INSTALL.md).

Install Pure Data with your package manager or get binaries
from:

  https://puredata.info/downloads/

You need the following externals to run tpf-server

  * aoo

You can install externals through the Pd menu:
`Help` -> `Find Externals`

NOTE: There is no official release of AoO yet. A release should
be available by the end of the year 2021.

### Run tpf-server

For the server to be reachable by the clients, it should run on
a machine with a public IP address. On a head-less machine, you
probably want to run it in nogui mode:

```
pd -nogui -open tpf-server/tpf-server.pd
```

The server opens a listening socket on port 12043 (both TCP and UDP).
Please make sure that this port is open in your firewall configuration.


### Issues

For any bug, issue or suggestion, please open an issue [here](https://github.com/zhdk/tpf-server/issues).

### Authors

  * Roman Haefeli <roman.haefeli@zhdk.ch>
  * Johannes Schütt <johannes.schuett@zhdk.ch>

### License

  GPL 3.0 (see LICENSE.txt)

