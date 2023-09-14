## tpf-server

NOTE: tpf-server is still in an experimental state and does not guarantuee
      backwards compatibility yet.


### About

**[tpf-server](https://github.com/zhdk/tpf-server)** connects instances of tpf-client.
Nowadays, tpf-server is simply **aooserver** from [AoO](https://git.iem.at/cm/aoo)
software.

**[tpf-client](https://github.com/zhdk/tpf-client)** is a low-latency audio
transmission software based on the [AoO](https://git.iem.at/cm/aoo)  (Audio-over-OSC)
protocol and built in Pure Data.


For more information visit:

  * https://github.com/zhdk/tpf-server
  * https://github.com/zhdk/tpf-client

The University of the Arts Zurich runs a publicly accessible tpf-server which may be
used for exploring tpf-client:

  * Hostname: **tpf-server.zhdk.ch**
  * Port:  **12043**

### Installation

#### Build aoo
If you want to run your own instance of the tpf-server, you need to build [AoO](https://git.iem.at/cm/aoo).
As of the time of this writing, there are no binaries available yet. Refer to the AoO documentation
for detailed info, but basically those steps should get you a working build (works for Debian
and derivatices):

  1. Install everything we need for building:

      ```
      sudo apt install git build-essential cmake
      ```

  2. Clone the aoo git repository:

      ```
      git clone https://git.iem.at/cm/aoo.git
      cd aoo
      git checkout develop
      git submodule update --init
      ```

  3. Configure the build (we don't need the Pure Data externals nor the SuperCollider extensions):

      ```
      mkdir build
      cd build
      cmake .. \
        -DAOO_BUILD_PD_EXTERNAL=OFF \
        -DAOO_BUILD_SC_EXTENSION=OFF \
        -DAOO_LOG_LEVEL=Warning \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DAOO_SYSTEM_OPUS=off \
        -DOPUS_BUILD_SHARED_LIBRARY=off
      ```

  4. Build the aoo binaries:

      ```
      make -j
      ```

  5. Install everything:

      ```
      make install
      ```

#### Configure aooserver as system daemon

If you want to run aooserver as system daemon that automatically
starts when the server boots and that can be managed like any
other systemd service, then follow these steps to configure aooserver
as tpf-server.service systemd unit:

  1. Add a system-user `tpf-server` which the daemon is going to run as:

      ```
      useradd -r -s /usr/sbin/nologin tpf-server
      ```

  2. Install the service unit file:

      ```
      sudo cp systemd/tpf-server.service /etc/systemd/system/
      ```

  3. Enable and start the tpf-server.service:

      ```
      systemctl daemon-reload
      systemd enable tpf-server.service
      systemd start tpf-server.service
      ```

  4. Check if tpf-server is running correctly:

      ```
      journalctl -f -u tpf-server.service
      ```

      The output of the above command should look similar to this:

      ```
      Sep 14 14:31:31 tpf-server systemd[1]: Started tpf-server.service - tpf-server.
      Sep 14 14:31:31 tpf-server aooserver[2042]: Listening on port 12043
      ```

Now you can manage tpf-server with the usual systemd commands:

  * Start: `systemctl start tpf-server.service`
  * Stop: `systemctl stop tpf-server.service`

##### Change port, enable/disable relaying
If you want your tpf-server to listen on a different port, apply your settings to the
systemd unit in `/etc/systemd/system/tpf-server.service` and repeat the steps in 3.

### Server options
Of course, you can invoke **aooserver** directly from the command line, which might be
convenient for testing different parameters. **aooserver** supports the following options:

  - `-p`, `--port`: port number (default = 7078)
  - `-r`, `--relay`: enable server relay
  - `-l`, `--log-level=LEVEL`:  set log level


