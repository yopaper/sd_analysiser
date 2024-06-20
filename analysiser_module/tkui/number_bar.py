
class NumberBar:
    def __init__(self, master, width:int=100, height:int=15) -> None:
        from . import tk
        self._main_frame = tk.Frame( master=master )
        self._title_label = tk.Label( self._main_frame )
        self._title_label.grid( column=0, row=0, padx=1 )
        self._bar_canvas = tk.Canvas( self._main_frame, width=width, height=height )
        self._bar_canvas.grid( column=1, row=0, padx=1 )
        self._number_label = tk.Label( self._main_frame )
        self._number_label.grid( column=2, row=0, padx=1 )
        self._canvas_width = width; self._canvas_height = height
    #--------------------------------------------------------------------------------------
    def grid( self, column:int, row:int ):
        self._main_frame.grid( column=column, row=row, padx=3, pady=3 )
    #--------------------------------------------------------------------------------------
    def get_frame(self):return self._main_frame
    #--------------------------------------------------------------------------------------
    def set_bar_length_rate(self, rate:float, bar_color:str="#AAAAAA", bg_color:str="#565656"):
        rate = min( rate, 1 )
        rate = max( rate, 0 )
        #assert rate>=0 and rate <=1, "rate 必須落在 0~1 之間"
        self._bar_canvas.delete("all")
        self._bar_canvas.create_rectangle(0, 0, self._canvas_width, self._canvas_height, fill=bg_color)
        self._bar_canvas.create_rectangle( 3, 3, self._canvas_width*rate-2, self._canvas_height-2, fill=bar_color )
    #--------------------------------------------------------------------------------------
    def set_title(self, title:str):
        self._title_label.config( text=title )
    #--------------------------------------------------------------------------------------
    def set_number(self, number):
        self._number_label.config( text=number )