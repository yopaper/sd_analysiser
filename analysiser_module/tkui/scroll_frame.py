from . import tk

class ScrollFrame( tk.Frame ):
    def __init__(self, master, width:int = 200, height:int = 200):
        super().__init__( master=master )
        self.canvas = tk.Canvas( master=self )
        
        self.scroll_bar = tk.Scrollbar( master=self, orient="vertical", command=self.canvas.yview )
        
        self.canvas_frame = tk.Frame( self.canvas )
        self.canvas_frame.bind( "<Configure>",
            lambda e: self.canvas.configure( scrollregion=self.canvas.bbox("all") )
        )
        self.canvas.create_window( (0, 0), window=self.canvas_frame, anchor="nw" )
        self.canvas.configure( yscrollcommand = self.scroll_bar.set )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack( side="right", fill="y" )
    #--------------------------------------------------------------------------
    def get_frame(self):return self.canvas_frame
#==============================================================================