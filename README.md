Boardfarm DOCSIS
----------------

This is the repo  that will contain DOCSIS specific tests and libraries for use for testing a docsis CM, CMTS, or other devices in a typical DOCSIS environment

To use this boardfarm plugin on Ubuntu, you must install:

```sh
# TCL for encoding of an MTA config file
sudo apt update
sudo apt install tcllib

# docsis for running docsis commands
sudo apt install automake libtool libsnmp-dev bison make gcc flex git libglib2.0-dev libfl-dev
git clone https://github.com/rlaager/docsis.git
cd docsis
./autogen.sh
./configure
make
sudo make install
```