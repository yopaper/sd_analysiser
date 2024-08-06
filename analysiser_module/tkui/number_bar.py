
class NumberBar:
    def __init__(self, master, width:int=100, height:int=12) -> None:
        from . import tk
        self._title_label = tk.Label( master )
        self._title_label.grid( column=0, row=0, padx=1, sticky="w" )
        self._bar_canvas = tk.Canvas( master, width=width, height=height )
        self._bar_canvas.grid( column=1, row=0, padx=1, sticky="ns" )
        self._number_label = tk.Label( master )
        self._number_label.grid( column=2, row=0, padx=1, sticky="w" )
        self._canvas_width = width; self._canvas_height = height
    #--------------------------------------------------------------------------------------
    def grid( self, column:int, row:int ):
        self._title_label.grid(column=column, row=row)
        self._bar_canvas.grid( column=column+1, row=row )
        self._number_label.grid( column=column+2, row=row )
    #--------------------------------------------------------------------------------------
    def set_bar_length_rate(self, rate:float, bar_color:str="#CCC", bg_color:str="#CCC"):
        rate = min( rate, 1 )
        rate = max( rate, 0 )
        #assert rate>=0 and rate <=1, "rate 必須落在 0~1 之間"
        self._bar_canvas.delete("all")
        self._bar_canvas.create_rectangle( 0, 0, self._canvas_width+1, self._canvas_height+1, fill=bg_color, outline="" )
        self._bar_canvas.create_rectangle( 0, 4, self._canvas_width*rate, self._canvas_height-3, fill=bar_color, outline="#FFFFFF" )
        
    #--------------------------------------------------------------------------------------
    def set_title(self, title:str):
        self._title_label.config( text=title )
    #--------------------------------------------------------------------------------------
    def set_number(self, number):
        self._number_label.config( text=number )