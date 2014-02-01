import ttybotron, urwid

class AsbListBoxWalker( object ):
    pass

class AsbListBox( urwid.ListBox ):
    def __init__( self ):
        body = urwid.SimpleFocusListWalker([])
        super( AsbListBox, self ).__init__( body )

    def add_message( self, packet, addr ):
        # Get the current position

class Asciibotron( object ):
    def __init__( self ):
        # Generate UI elements
        #self.wdg_cols_top = urwid.Columns([])
        self.wdg_list_msg = urwid.ListBox([])
        #self.wdg_frame = urwid.Frame(
        #    header = self.wdg_cols_top,
        #    body = self.wdg_list_msg
        #)

        # Set up the message listening
        self.socket = ttybotron.make_socket( 17892 )
        self.recvr = ttybotron.SDPPrintReceiver( self.socket, self.receive )
        self.messages = []
    
    def __call__( self ):
        self.loop = urwid.MainLoop(
        #    self.wdg_frame
            self.wdg_list_msg,
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
