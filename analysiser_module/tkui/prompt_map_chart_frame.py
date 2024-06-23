from . import tk

class MapText:
    def __init__(self, prompt:str, redundant_rate:float, lack_rate:float, item_index:int, button:tk.Button ):
        self.prompt = prompt
        self.redundant_rate = redundant_rate
        self.lack_rate = lack_rate
        self.item_index = item_index
        self.enable = True
        self.button = button
#====================================================================================================
class PromptMapChartFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self._padding = 20
        self._canvas_width = 500
        self._canvas_height = 500
        self._map_canvas = tk.Canvas(
            self,
            width=self._canvas_width + 2*self._padding,
            height=self._canvas_height + 2*self._padding
        )
        self._map_canvas.grid( column=0, row=0 )
        self._button_frame = tk.LabelFrame( self, text="顯示/隱藏" )
        self._button_frame.grid( column=1, row=0, padx=8, pady=8 )

        self._text_table:dict[str, MapText] = {}

        self._min_redundant_rate = -0.1
        self._max_redundant_rate = 0.1
        self._min_lack_rate = -0.1
        self._max_lack_rate = 0.1
        self._map_canvas.delete()
    #----------------------------------------------------------------------
    def reset(self):
        for key in self._text_table:
            self._text_table[ key ].button.destroy()
        self._text_table.clear()
        self._min_redundant_rate = -0.1
        self._max_redundant_rate = 0.1
        self._min_lack_rate = -0.1
        self._max_lack_rate = 0.1
        self._map_canvas.delete( "all" )
    #----------------------------------------------------------------------
    def load_processor(self, processor):
        from .. import analysiser, prompt_tag
        processor:analysiser.analysiser_processor.AnalysiserProcessor = processor
        data_table:dict[str, tuple[int, int]] = {}
        #.............................................................
        def add_unifier( prompt:str, unifier:analysiser.result_value_unifier.ResultValueUnifier):
            if( unifier == None ):return
            redundant_rate = unifier.get_avg_redundant_rate()
            lack_rate = unifier.get_avg_lack_rate()
            if( redundant_rate==None ):redundant_rate = 0
            if( lack_rate==None ):lack_rate = 0
            value_padding = 0.05
            self._max_redundant_rate = max( self._max_redundant_rate, redundant_rate + value_padding )
            self._min_redundant_rate = min( self._min_redundant_rate, redundant_rate - value_padding )
            self._max_lack_rate = max( self._max_lack_rate, lack_rate + value_padding )
            self._min_lack_rate = min( self._min_lack_rate, lack_rate - value_padding )
            data_table[ prompt ] = (redundant_rate, lack_rate)
        #.............................................................
        self.reset()
        all_prompts = prompt_tag.get_all_prompts()
        for prompt in all_prompts:
            unifier = processor.get_unifier_with_prompt_group( prompt=prompt )
            add_unifier( prompt=prompt, unifier=unifier )
        # Draw Chart
        redundant_delta = self._max_redundant_rate - self._min_redundant_rate
        lack_delta = self._max_lack_rate - self._min_lack_rate
        chart_left = self._padding; chart_right = chart_left + self._canvas_width
        chart_top = self._padding; chart_bottom = chart_top + self._canvas_height
        redundant_zero_line = chart_left + self._canvas_width * abs( self._min_redundant_rate ) / (self._max_redundant_rate - self._min_redundant_rate)
        lack_zero_line = chart_top + self._canvas_height * abs( self._max_lack_rate ) / (self._max_lack_rate - self._min_lack_rate)
        
        self._map_canvas.create_line( redundant_zero_line, chart_top, redundant_zero_line, chart_bottom, fill="#BBBBBB", dash=(1, 1) )
        self._map_canvas.create_line( chart_left, lack_zero_line, chart_right, lack_zero_line, fill="#BBBBBB", dash=(1, 1) )
        self._map_canvas.create_rectangle( chart_left, chart_top, chart_right, chart_bottom, outline="#AAAAAA" )
        self._map_canvas.create_text( chart_right, chart_bottom, text="提示詞多餘", anchor="ne" )
        self._map_canvas.create_text( chart_left, chart_top, text="提示詞缺失", anchor="sw" )
        print( self._max_redundant_rate, self._min_redundant_rate, self._max_lack_rate, self._min_lack_rate )
        for prompt in data_table:
            redundant_rate, lack_rate = data_table[ prompt ]
            x = ( ( redundant_rate - self._min_redundant_rate ) / redundant_delta )*self._canvas_width + chart_left
            y = chart_bottom - ( ( lack_rate - self._min_lack_rate ) / lack_delta )*self._canvas_height
            button = tk.Button( self._button_frame, text=prompt, command=lambda key=prompt:self.switch_text_enable(key) )
            button.pack(side="top", padx=4, pady=4, fill="x")
            text_index = self._map_canvas.create_text( x, y, text=prompt )
            map_text = MapText(
                prompt=prompt,
                redundant_rate=redundant_rate,
                lack_rate=lack_rate,
                item_index=text_index,
                button=button
            )
            self._text_table[ prompt ] = map_text
    #----------------------------------------------------------------------
    def switch_text_enable(self, prompt:str):
        text = self._text_table[ prompt ]
        text.enable = not text.enable
        text_index = text.item_index
        if( text.enable ):
            self._map_canvas.itemconfig( text_index, state="normal" )
        else:self._map_canvas.itemconfig( text_index, state="hidden" )
#=======================================================================