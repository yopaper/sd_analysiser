from . import tk

class ScrollFrame( tk.Frame ):
    def __init__(self, master, width:int = 200, height:int = 200):
        super().__init__( master=master )
        self.canvas = tk.Canvas( master=self, width=width, height=height )
        
        self.scroll_bar_v = tk.Scrollbar( master=self, orient="vertical", command=self.canvas.yview )
        self.scroll_bat_h = tk.Scrollbar( master=self, orient="horizontal", command=self.canvas.xview )
        
        self.canvas_frame = tk.Frame( self.canvas )
        
        self.canvas.create_window( (0, 0), window=self.canvas_frame, anchor="nw" )
        self.canvas.configure( yscrollcommand = self.scroll_bar_v.set, xscrollcommand = self.scroll_bat_h.set )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar_v.pack( side="right", fill="y" )
        self.scroll_bat_h.pack( side="bottom", fill="x" )
    #--------------------------------------------------------------------------
    def update_scrollregion(self):
        self.canvas.after( 1000, lambda:self.canvas.configure( scrollregion=self.canvas.bbox("all") ) )
    #--------------------------------------------------------------------------
    def get_frame(self):return self.canvas_frame
#==============================================================================