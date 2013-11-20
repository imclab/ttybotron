"""
TTYBOTRON
=========
A TTY Tubotron.

.. todo::
 * Command line args for:
   * Port to listen on
   * Filtering by IP, chip, core, etc.
"""

import socket, struct, sys

def ttybotron( port = 50000 ):
    """Continue to poll an incoming socket on the appropriate port and print
    out a formatted string of the machine, chip, core and message."""
    # Set up the socket
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind( ( "", port ) )

    try:
        while True:
            # Grab the stuff from the socket
            (data, addr) = sock.recvfrom( 1024 ) # Socket size is 1024 bytes

            # Unpack the data
            header = data[2:2+8]
            command = data[2+8:2+8+16]
            data = data[2+8+16:]
    
            # Unpack the header
            (flags, iptag, dest_port, srce_port, dest_addr, srce_addr) = (
                struct.unpack( "!4B 2H", header ) )
    
            (chip_x, chip_y) = (
                struct.unpack( "2B", struct.pack( "H", srce_addr ) ) )
    
            (cmdrc, arg1, arg2, arg3) = struct.unpack( "4I", command )
    
            core = srce_port & 0x1f
    
            # Reverse look up the DNS for the incoming SpiNNaker board
            hn = socket.gethostbyaddr( addr )

            # Now output any desired information
            sys.stdout.write( "%15s\t% 2d % 2d % 2d\t%s" % (
                                hn, core, chip_x, chip_y, data
                            )
            )
    finally:
        sys.stderr.write("\nEnd.")
        sock.close()

if __name__ == "__main__":
    ttybotron( )
