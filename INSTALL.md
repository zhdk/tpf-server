Installation
============

Yet, there exists only detailed instructions for setting up a **tpf-server**
for Debian and Ubuntu. 

Debian / Ubuntu
===============


The following commands are meant to be executed as root. First,
we need to install all dependencies with the package manager. All
externals required for tpf-server have been packaged by Debian
maintainers, which makes the process quite straight-forward.

```bash
apt install puredata pd-osc pd-iemnet pd-slip git python3
```

Then, we install the **tpf-server** from our Gitlab to /opt/tpf-server:

```bash
cd /opt
git clone --recursive https://gitlab.zhdk.ch/TPF/tpf-server
```

Now, we are already able to run the tpf-server with the following command:

```bash
pd -nogui -nomidi -nosound -open /opt/tpf-server/tpf-server.pd
```

The output should look similar to:

```
slipdec: maximum packet length is 16384
slipdec: maximum packet length is 16384
iemnet - networking with Pd: [tcpserver]
        version 0.2.2
        compiled on Mar 31 2020 at 22:35:18
        copyright © 2010-2015 IOhannes m zmoelnig, IEM
        based on mrpeach/net, based on maxlib
slipenc: maximum packet length is 16384
```

But let's turn that to a systemd service proper, so that it is
automatically run at system startup and can be started and stopped as a
normal system service.

Let's run tpf-server as a separate system user named tpf-server. 
So, let's create that user first:

```bash
useradd -r -s /usr/sbin/nologin tpf-server
```

We create a systemd service unit file for tpf-server at
`/etc/systemd/system/tpf-server.service` with our favorite text editor:

```bash
nano /etc/systemd/system/tpf-server.service  
```

with the following content:

```systemd
[Unit]
Description=tpf-server
After=syslog.target

[Service]
Type=simple
ExecStart=/usr/bin/pd \
   -nogui -noaudio -nomidi -nrt \
   -open /opt/tpf-server/tpf-server.pd
User=tpf-server
Group=tpf-server

[Install]
WantedBy=multi-user.target
```

Now, we enable and start the newly created service:

```bash
systemctl daemon-reload
systemctl enable tpf-server.service
systemctl start tpf-server.service
```

If everything goes right, we see the service in a 'started' state:

```
systemctl status tpf-server.service
```

The output should look like this:

```
● tpf-server.service - tpf-server
   Loaded: loaded (/etc/systemd/system/tpf-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-04-08 11:58:20 CEST; 1 day 7h ago
 Main PID: 430 (pd)
    Tasks: 1 (limit: 4673)
   Memory: 13.1M
   CGroup: /system.slice/tpf-server.service
           └─430 /usr/bin/pd -nogui -noaudio -nomidi -nrt -open /opt/tpf-server/tpf-server.pd
```

Now, we have the management part of the tpf-server up and running. It
listens on the TCP port 3025. However, the audio transmission uses an
UDP proxy written in Python. For this, we create another systemd
service.


Create the file /etc/systemd/system/tpf-udp-proxy.service:

```bash
nano /etc/systemd/system/tpf-udp-proxy.service
```

with the content:

```systemd
[Unit]
Description=UDP dynamic proxy for tpf-server
After=syslog.target

[Service]
Type=simple
ExecStart=python /opt/tpf-server/tpf-udp-proxy.py
User=tpf-server
Group=tpf-server

[Install]
WantedBy=multi-user.target
```

We enable and start the service with the same command sequence:

```bash
systemctl daemon-reload
systemctl enable tpf-udp-proxy.service
systemctl start tpf-udp-proxy.service
```
We can see that the udp proxy is up and running with:

```bash
systemctl status tpf-udp-proxy.service
```

The output should look like:

```
● tpf-udp-proxy.service - UDP dynamic proxy for tpf-server
   Loaded: loaded (/etc/systemd/system/tpf-udp-proxy.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-04-08 11:58:20 CEST; 1 day 7h ago
 Main PID: 442 (python)
    Tasks: 1 (limit: 4673)
   Memory: 3.7M
   CGroup: /system.slice/tpf-udp-proxy.service
           └─442 /usr/bin/python /opt/tpf-server/tpf-udp-proxy.py
```

This service listens on the UDP port 4460 and is used solely for
proxying jacktrip packets.

When both services are running, your **tpf-server** is ready.

Firewall
========

Make sure that your firewall allows incoming traffic on the following ports:

  * 3025/TCP
  * 4460/UDP


