"""
TTYBOTRON
=========
A TTY Tubotron.

.. todo::
   * curses interface
"""

import argparse, socket, string, struct, sys, threading, time

def make_socket( port ):
    """Make an appropriate socket for receiving SDP packets.

    :param port: Port to listen on.
    :returns: An open socket.
    """
    # Instantiate the socket, set non-blocking
    _socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    _socket.setblocking( 0 )
    _socket.bind( ( "", port ) )
    return _socket

class SDPPrintPacket( object ):
    """An SDP Packet as generated by the spin1_printf or similar function.

    :param data: An array of bytes as received from a socket.
    :type data: array
    """
    def __init__( self, data ):
        # Process the data and save
        header = data[0:2+8]
        self.data = data[2+8+4:]

        ( self.flags, self.iptag, self.dest_port, self.srce_port,
          self.dest_addr, self.chip_x, self.chip_y ) = ( 
          struct.unpack( "!2x 4B H 2B", header )
        )
   
        self.core = self.srce_port & 0x1f

class SDPPrintReceiver( threading.Thread ):
    """Creates a thread which keeps trying to receive SDP messages.  When a 
    message is received the provided callback is called with the message.

    :param socket: Socket to check.
    :param callback: Function to call when a packet is received.
    """
    def __init__( self, socket, callback ):
        # Call super
        super( SDPPrintReceiver, self ).__init__()

        # Save the socket and callback
        self._socket = socket
        self._callback = callback

        # State
        self.exit = False

    def run( self ):
        # Run as long as we can...
        while not self.exit:
            # Try to receive a packet
            try:
                ( data, addr ) = self._socket.recvfrom( 1024 )

                # Call the callback with the packet
                packet = SDPPrintPacket( data )
                self._callback( packet, addr )
            except IOError: # There was nothing to get
                pass
            finally:
                time.sleep( 0.1 )

def ttybotron( args = None ):
    """Continue to poll an incoming socket on the appropriate port and print
    out a formatted string of the machine, chip, core and message."""
    # Retrieve some options from args, construct output strings
    field_bs = [not x for x in
                   [args.no_host, args.no_chip, args.no_chip, args.no_core]
               ]

    if args.headers:
        hs = [ str.ljust( "Host", 15 ), " X", " Y", " C" ]
        h_fields = [h for (h,b) in zip(hs, field_bs) if b]

        sys.stdout.write( "# %s  Message\n" % string.join( h_fields, ", " ) )
        sys.stdout.flush()

    # Set up the socket
    if args.verbose:
        sys.stderr.write( ".. Creating socket\n" )
    sock = make_socket( args.port )

    # Create a call back function
    def printer( packet, addr ):
        """Prints an SDP Packet."""
        ( ip, port ) = addr
        if not args.no_dns:
            ( host, aliases, ips ) = socket.gethostbyaddr( ip )
        else:
            host = "%15s" % ip

        hs = [ str.ljust( host, 15 )[:15], "%2d" % packet.chip_x,
               "%2d" % packet.chip_y, "%2d" % packet.core ]
        h_fields = [h for (h,b) in zip(hs, field_bs) if b]

        sys.stdout.write( "( %s) %s\n" % (
                            string.join( h_fields, ", " ),
                            packet.data
                        )
        )
        sys.stdout.flush()

    try:
        # Make and run the socket receiving thread
        if args.verbose: sys.stderr.write( ".. Starting receiver thread\n" )
        recvr = SDPPrintReceiver( sock, printer )
        recvr.start()

        if args.verbose: sys.stderr.write( ".. Waiting for packets...\n" )

        while True:
            pass
    except KeyboardInterrupt:
        recvr.exit = True
        if args.verbose: sys.stderr.write( ".. Terminating receiver thread\n" )
    finally:
        # Wait for the receiver, close the socket
        recvr.join()
        if args.verbose: sys.stderr.write( ".. Closing socket\n" )
        sock.close()

        # Flush outputs
        if args.verbose: sys.stderr.write( ".. Flushing output" )
        sys.stdout.flush()
        sys.stderr.write("\n")
        sys.stderr.flush()

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser( description='Display printf output '\
                                      'from SpiNNaker machines.' )
    parser.add_argument( "-v", "--verbose", help="display verbose status",
                         action="store_true" )
    parser.add_argument( "-p", "--port", help="listen on the given port",
                         default=17892, type=int )
    igroup = parser.add_mutually_exclusive_group()
    igroup.add_argument( "-i", "--interactive", help="run an interactive " \
                          "instance using curses", action="store_true" )
    parser.add_argument( "-t", "--headers", help="print the table header",
                         action="store_true" )
    parser.add_argument( "--no-host", help="don't display the host field",
                         action="store_true" )
    parser.add_argument( "--no-chip", help="don't display the chip x or y",
                         action="store_true" )
    parser.add_argument( "--no-core", help="don't display the core field",
                         action="store_true" )
    parser.add_argument( "--no-dns", "--nd", help="don't use DNS loop up " \
                         "for the hostname, just print the IP address",
                         action="store_true" )

    # Parse the arguments
    args = parser.parse_args()

    if args.interactive:
        raise NotImplementedError
    else:
        ttybotron( args = args )
