
class ResultNumberBarGroup:
    def __init__(self, master, title:str="", has_score_bar:bool=False):
        from . import tk, number_bar
        self._main_frame = tk.LabelFrame( master=master, text=title )
        self._bar_frame = tk.Frame( self._main_frame )
        self._bar_frame.pack()

        self._has_score_bar = has_score_bar
        self._score_bar : number_bar.NumberBar = None
        grid_row = 0
        if( has_score_bar ):
            self._score_bar = number_bar.NumberBar( self._bar_frame )
            self._score_bar.set_title("％Confidence")
            self._score_bar.grid(column=0, row=grid_row)
            grid_row += 1
        self._correct_bar = number_bar.NumberBar( self._bar_frame )
        self._correct_bar.grid(column=0, row=grid_row)
        self._correct_bar.set_title("✓Correct")
        grid_row += 1

        self._redundant_bar = number_bar.NumberBar( self._bar_frame )
        self._redundant_bar.grid(column=0, row=grid_row)
        self._redundant_bar.set_title("＋Redundant")
        grid_row += 1

        self._lack_bar = number_bar.NumberBar( self._bar_frame )
        self._lack_bar.grid(column=0, row=grid_row)
        self._lack_bar.set_title("－Lack")
        grid_row += 1
        self.reset()
    #-------------------------------------------------------------------------
    def get_frame(self):return self._main_frame
    #-------------------------------------------------------------------------
    def reset(self):
        from . import number_bar
        def reset_bar( bar:number_bar.NumberBar ):
            bar.set_bar_length_rate(0, "#666666")
            bar.set_number( "No Data" )
        #...................................................................
        if( self._has_score_bar ):
            reset_bar( self._score_bar )
        reset_bar( self._correct_bar )
        reset_bar( self._redundant_bar )
        reset_bar( self._lack_bar )
    #------------------------------------------------------------------------------------------------
    def set_bar_value(self, score:float, correct_rate:float, redundant_rate:float, lack_rate:float):
        def to_percent(value)->str:
            value = round( value*1e2 )
            return "{0}%".format( value )
        #..............................................................
        def get_bar_color(value)->str:
            if( value >= 0.8 ):return "#44FF44"
            elif( value >= 0.7 ):return "#66CC44"
            elif( value >= 0.6 ):return "#77AA44"
            elif( value >= 0.5 ):return "#998844"
            elif( value >= 0.4 ):return "#AA7744"
            elif( value >= 0.3 ):return "#CC5544"
            elif( value >= 0.2 ):return "#FF4444"
            else:return "#FF0000"
        #...............................................................
        # Score
        if( self._has_score_bar ):
            self._score_bar.set_bar_length_rate( rate=score, bar_color="#999" )
            self._score_bar.set_number( to_percent( score ) )
        # Correct Rate
        bar_color = get_bar_color( correct_rate )
        self._correct_bar.set_bar_length_rate( rate=correct_rate, bar_color=bar_color )
        self._correct_bar.set_number( to_percent( correct_rate ) )
        # Redundant Rate
        if( redundant_rate != None ):
            bar_color = get_bar_color( 1-redundant_rate )
            self._redundant_bar.set_bar_length_rate( rate=redundant_rate, bar_color=bar_color )
            self._redundant_bar.set_number( to_percent( redundant_rate ) )
        else:
            self._redundant_bar.set_bar_length_rate(rate=1, bar_color="#FFFFFF" )
            self._redundant_bar.set_number("None")
        # Lack Rate
        if( lack_rate != None ):
            bar_color = get_bar_color( 1-lack_rate )
            self._lack_bar.set_bar_length_rate( rate=lack_rate, bar_color=bar_color )
            self._lack_bar.set_number( to_percent( lack_rate ) )
        else:
            self._lack_bar.set_bar_length_rate( rate=1, bar_color="#FFFFFF" )
            self._lack_bar.set_number("None")
    #------------------------------------------------------------------------------------------------
    def load_unifier(self, unifier):
        from .. import analysiser
        unifier:analysiser.result_value_unifier.ResultValueUnifier = unifier
        self.set_bar_value(
            score=0,
            correct_rate=unifier.get_avg_correct_rate(),
            redundant_rate=unifier.get_avg_redundant_rate(),
            lack_rate=unifier.get_avg_lack_rate(),
        )
    #------------------------------------------------------------------------------------------------
    def load_result(self, result):
        from .. import analysiser
        result:analysiser.process_result.ProcessResult = result
        self.set_bar_value(
            score=result.get_score(),
            correct_rate=result.get_correct_rate(),
            redundant_rate=result.get_redundant_rate(),
            lack_rate=result.get_lack_rate(),
        )
#==============================================================================================