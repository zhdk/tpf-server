## tpf-server

### About

**[tpf-server](https://github.com/zhdk/tpf-server)** connects instances of tpf-client.

Historically, tpf-server was running as Pd patch. Nowadays, tpf-server is simply **aooserver**
from the [AoO](https://git.iem.at/aoo/aoo) software.

**[tpf-client](https://github.com/zhdk/tpf-client)** is a low-latency audio
transmission software based on the [AoO](https://git.iem.at/cm/aoo)  (Audio-over-OSC)
protocol and built in Pure Data.


For more information visit:

  * https://github.com/zhdk/tpf-server
  * https://github.com/zhdk/tpf-client
  * https://git.iem.at/aoo/aoo

The University of the Arts Zurich runs a publicly accessible tpf-server which may be
used for exploring tpf-client:

  * Hostname: **tpf-server.zhdk.ch**
  * Port:  **27001**

### Installation

You can get AoO builds containing the `aooserver` binary from [here](https://git.iem.at/aoo/aoo/-/releases).
Select the build matching your platform from the 'Binaries' section.



#### Configure aooserver as system daemon

If you want to run aooserver as system daemon that automatically
starts when the server boots and that can be managed like any
other systemd service, then follow these steps to configure aooserver
as tpf-server.service systemd unit:

  1. Add a system-user `tpf-server` which the daemon is going to run as:

      ```
      sudo useradd -r -s /usr/sbin/nologin tpf-server
      ```

  2. Install the service unit file:

      ```
      sudo cp systemd/tpf-server.service /etc/systemd/system/
      ```

  3. Enable and start the tpf-server.service:

      ```
      sudo systemctl daemon-reload
      sudo systemctl enable tpf-server.service
      sudo systemctl start tpf-server.service
      ```

  4. Check if tpf-server is running correctly:

      ```
      sudo journalctl -f -u tpf-server.service
      ```

      The output of the above command should look similar to this:

      ```
      Sep 14 14:31:31 tpf-server systemd[1]: Started tpf-server.service - tpf-server.
      Sep 14 14:31:31 tpf-server aooserver[2042]: Listening on port 27001
      ```

Now you can manage tpf-server with the usual systemd commands:

  * Start: `sudo systemctl start tpf-server.service`
  * Stop: `sudo systemctl stop tpf-server.service`

##### Change port, enable/disable relaying
If you want your tpf-server to listen on a different port, apply your settings to the
systemd unit in `/etc/systemd/system/tpf-server.service` and repeat the steps in 3.

### Server options
Of course, you can invoke **aooserver** directly from the command line, which might be
convenient for testing different parameters. **aooserver** supports the following options:

  - `-p`, `--port=PORT`: port number (default = 7078)
  - `-r`, `--relay`: enable server relay
  - `-l`, `--log-level=LEVEL`:  set log level


