ttybotron
=========

A TTY Tubotron for SpiNNaker

Usage: ```ttybotron.py [-h] [-v] [-p PORT] [-i] [-t] [--no-host] [--no-chip]
                       [--no-core] [--no-dns]```

Display printf output from SpiNNaker machines.

Option(s)                         | Effect
--------------------------------- | -----------------------------------------------------------------
 ```-h```, ```--help```           | show this help message and exit
 ```-v```, ```--verbose```        | display verbose status
 ```-p PORT```, ```--port PORT``` | listen on the given port
 ```-i```, ```--interactive```    | run an interactive instance using curses
 ```-t```, ```--headers```        | print the table header
 ```--no-host```                  | don't display the host field
 ```--no-chip```                  | don't display the chip x or y
 ```--no-core```                  | don't display the core field
 ```--no-dns```, --nd             | don't use DNS loop up for the hostname, just print the IP address

Installation
------------

You can install ttybotron by running the following as root:

```bash
# python setup.py install
```

ttybotron can then be run by any user with the command:

```bash
$ ttybotron.py
```


Troubleshooting
---------------

If you think you should be receiving packets and aren't you should:

1. Run ttybotron with the ```--no-dns``` option: ```ttybotron.py --nd```
2. Check that your firewall is accepting UDP packets on port 17892
