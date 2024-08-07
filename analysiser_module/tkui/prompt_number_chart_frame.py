from . import tk

class ChartCanvas(tk.Canvas):
    def __init__(self, master, width:int=350, height:int=300):
        self._left_padding = 2
        self._bottom_padding = 20
        self._top_padding = 20
        super().__init__( master=master,
                         width = width + self._left_padding,
                         height = height + self._bottom_padding + self._top_padding )
        self._data_table:dict[int, float] = {}
        self._canvas_width = width
        self._canvas_height = height
        self._max_key=None; self._min_key=None
        self._max_data=1; self._min_data=0
        self._data_title = "Y"
        self._key_title = "X"
    #-----------------------------------------------------------------------------
    def reset(self):
        self._max_key=None; self._min_key=None
        self._max_data=1; self._min_data=0
        self._data_table.clear()
    #-----------------------------------------------------------------------------
    def set_data(self, key, data):
        if( data==None ):return
        self._data_table[key] = data
        if( self._max_key == None or key > self._max_key ):
            self._max_key = key
        if( self._min_key == None or key < self._min_key ):
            self._min_key = key
        if( self._max_data == None or data > self._max_data ):
            self._max_data = data
        if( self._min_data==None or data < self._min_data ):
            self._min_data = data
    #-----------------------------------------------------------------------------
    def set_title( self, data_title:str, key_title:str ):
        self._data_title = data_title
        self._key_title = key_title
    #-----------------------------------------------------------------------------
    def draw_chart(self):
        self.delete("all")
        if( len( self._data_table )<=0 ):return
        key_delta = self._max_key - self._min_key + 1
        data_delta = self._max_data - self._min_data
        bar_width = round(self._canvas_width / key_delta)

        chart_left = self._left_padding
        chart_right = self._left_padding + self._canvas_width
        chart_top = self._top_padding
        chart_bottom = self._top_padding + self._canvas_height

        zero_line = chart_top + self._canvas_height * self._max_data / data_delta

        for key in self._data_table:
            data = self._data_table[ key ]
            x1 = (key - self._min_key + 0.15) * bar_width + self._left_padding
            x2 = x1 + bar_width * 0.7
            y1 = (1 - ( ( data - self._min_data ) / data_delta) ) * self._canvas_height + self._top_padding
            y2 = zero_line
            self.create_rectangle( x1, y1, x2, y2, fill="#666666", outline="#999999" )
        self.create_rectangle(
            chart_left, chart_top, chart_right, chart_bottom, outline="#999999"
        )
        self.create_text(
            chart_right,
            chart_bottom,
            text = " [{0}~{1}] <{2}> ".format( self._min_key, self._max_key , self._key_title ),
            anchor="ne"
        )
        self.create_text(
            chart_left, chart_top,
            text = " [{0}~{1}] <{2}> ".format( round(self._min_data*1e2)/1e2, round(self._max_data*1e2)/1e2, self._data_title ),
            anchor="sw"
        )
#=================================================================================

class PromptNumberChartFrame( tk.Frame ):
    def __init__(self, master):
        super().__init__(master=master)
        pady = 8
        self._correct_rate_chart = ChartCanvas( self )
        self._correct_rate_chart.set_title(
            data_title="Prompts Correct",
            key_title="Prompts Number"
        )
        self._correct_rate_chart.grid( column=0, row=0, padx=5, pady=pady )
        self._redundant_rate_chart = ChartCanvas( self )
        self._redundant_rate_chart.set_title(
            data_title="Prompts Redundant",
            key_title="Prompts Number"
        )
        self._redundant_rate_chart.grid( column=0, row=1, padx=5, pady=pady )
        self._lack_rate_chart = ChartCanvas( self )
        self._lack_rate_chart.set_title(
            data_title="Prompts Lack",
            key_title="Prompts Number"
        )
        self._lack_rate_chart.grid( column=0, row=2, padx=5, pady=pady )

    #----------------------------------------------------------------------------
    def load_processor(self, processor):
        from .. import analysiser
        processor:analysiser.analysiser_processor.AnalysiserProcessor = processor
        number_key = processor.get_prompt_number_table_key()
        self._correct_rate_chart.reset()
        self._redundant_rate_chart.reset()
        self._lack_rate_chart.reset()
        for key in number_key:
            unifier = processor.get_unifiier_with_prompt_number( key )
            self._correct_rate_chart.set_data( key=key, data=unifier.get_avg_correct_rate() )
            self._redundant_rate_chart.set_data( key=key, data=unifier.get_avg_redundant_rate() )
            self._lack_rate_chart.set_data( key=key, data=unifier.get_avg_lack_rate() )
        self._correct_rate_chart.draw_chart()
        self._redundant_rate_chart.draw_chart()
        self._lack_rate_chart.draw_chart()
#================================================================================
