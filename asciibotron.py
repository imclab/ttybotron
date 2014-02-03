import sys, ttybotron

try:
    import urwid
except:
    sys.stderr.write( "Failed to import urwid, you must install urwid.\n" )
    sys.exit( -1 )

class AsbListBoxWalker( object ):
    pass

class AsbListBox( urwid.ListBox ):
    def __init__( self ):
        body = urwid.SimpleFocusListWalker([])
        super( AsbListBox, self ).__init__( body )

    def add_message( self, packet, addr ):
        lbl_host = ""
        lbl_x = urwid.Text( "%d" % packet.chip_x, align="right" )
        lbl_y = urwid.Text( "%d" % packet.chip_y, align="right" )
        lbl_c = urwid.Text( "%d" % packet.core, align="right" )
        lbl_message = urwid.Text( packet.data )

        clms = urwid.Columns([
            (10, lbl_host),
            ( 3, lbl_x),
            ( 3, lbl_y),
            ( 3, lbl_c),
            lbl_message
        ])

        self.append( clms )

class Asciibotron( object ):
    def __init__( self ):
        ## Generate UI elements
        self._palette = [
            ('header', 'white, bold', 'light blue'),
        ]

        # Labels for the columns
        self._lbl_host = urwid.Text( "Host" )
        self._lbl_x = urwid.Text( "X", align="right" )
        self._lbl_y = urwid.Text( "Y", align="right" )
        self._lbl_c = urwid.Text( "C", align="right" )
        self._lbl_message = urwid.Text( "Message" )

        # Header for the table
        self.wdg_cols_top = urwid.Columns([
            (10, self._lbl_host ),
            ( 3, self._lbl_x ),
            ( 3, self._lbl_y ),
            ( 2, self._lbl_c ),
            self._lbl_message,
        ], dividechars = 1)
        map1 = urwid.AttrMap( self.wdg_cols_top, 'header' )

        # List box
        self.wdg_list_msg = AsbListBox()

        # Frame
        self.wdg_frame = urwid.Frame(
            header = map1,
            body = self.wdg_list_msg
        )

        ## Set up the message listening
        self.socket = ttybotron.make_socket( 17892 )
        self.recvr = ttybotron.SDPPrintReceiver( self.socket,
            self.wdg_list_msg.add_message )
        self.messages = []
    
    def __call__( self ):
        self.loop = urwid.MainLoop(
            self.wdg_frame,
            self._palette,
            unhandled_input = self.unhandled
        )
        self.recvr.start( )
        self.loop.run( )

    def unhandled( self, input ):
        if input in ['q', 'Q']:
            self.recvr.exit = True
            self.recvr.join()
            raise urwid.ExitMainLoop

if __name__ == "__main__":
    tron = Asciibotron( )
    tron()
