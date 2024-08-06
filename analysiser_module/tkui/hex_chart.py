
from . import tk

class HexChart( tk.Canvas ):
    def __init__(self, master, width:int=400, height:int=400):
        super().__init__( master=master, width=width, height=height )
        self.hex_radius = 165
        self.chart_width = width
        self.chart_height = height
        self.data_table:dict[ str, float ] = {}
        self.max_value = 1
        self.min_value = 0
        self.title = ""
    #----------------------------------------------------------------------------
    def data_number(self)->int:
        return len( self.data_table )
    #----------------------------------------------------------------------------
    def add_data(self, key:str, value:float)->None:
        if( value == None ):return
        self.data_table[ key ] = value
        if( value > self.max_value ):self.max_value = value
        if( value < self.min_value ):self.min_value = value
    #----------------------------------------------------------------------------
    def set_title(self, title:str):
        self.title = title
    #----------------------------------------------------------------------------
    def reset(self, min_value:float=0, max_value:float=1):
        self.max_value = max_value
        self.min_value = min_value
        self.data_table.clear()
    #----------------------------------------------------------------------------
    def draw_chart(self):
        from math import pi, cos, sin
        self.delete("all")
        if( self.data_number()<=2 ):return
        center_pos = ( self.chart_width/2, self.chart_height/2 )
        step_degree = 2 * pi / self.data_number()
        max_min_delta = self.max_value - self.min_value
        #.................................................
        def get_hex_point(index)->tuple[int, int]:
            degree = index * step_degree
            point_x = center_pos[0] + cos(degree) * self.hex_radius
            point_y = center_pos[1] + sin(degree) * self.hex_radius
            return( point_x, point_y )
        #.................................................
        out_polygon_pos = []
        for i in range( self.data_number() ):
            x, y = get_hex_point(i)
            out_polygon_pos.append(x)
            out_polygon_pos.append(y)
        self.create_polygon( out_polygon_pos, outline="#CCC", fill="" )
        
        i = 0
        in_polygon_pos = []
        for key in self.data_table:
            x, y = get_hex_point(i)
            value = self.data_table[ key ]
            value_rate = (value-self.min_value) / max_min_delta
            x = x * value_rate + center_pos[0] * (1-value_rate)
            y = y * value_rate + center_pos[1] * (1-value_rate)
            in_polygon_pos.append( x )
            in_polygon_pos.append( y )
            i += 1
        self.create_polygon( in_polygon_pos, fill="#CCC" )
            
        i = 0
        for key in self.data_table:
            x, y = get_hex_point(i)
            value = self.data_table[key]
            value = round(value*100)/1
            self.create_text( x, y, text=key, anchor="s" )
            self.create_text( x, y, text="{0}%".format(value), anchor="n" )
            i += 1
        self.create_text( *center_pos, text=self.title )
#================================================================================