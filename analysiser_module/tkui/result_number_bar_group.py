
class ResultNumberBarGroup:
    def __init__(self, master, title:str="", has_score_bar:bool=False):
        from . import tk, number_bar
        self._main_frame = tk.LabelFrame( master=master, text=title )
        self._has_score_bar = has_score_bar
        self._score_bar : number_bar.NumberBar = None
        if( has_score_bar ):
            self._score_bar = number_bar.NumberBar( self._main_frame )
            self._score_bar.set_title("信心分數")
            self._score_bar.get_frame().pack( side="top", padx=3, pady=3 )
        self._correct_bar = number_bar.NumberBar( self._main_frame )
        self._correct_bar.get_frame().pack( side="top", padx=3, pady=3 )
        self._correct_bar.set_title("提示詞正確率")
        self._redundant_bar = number_bar.NumberBar( self._main_frame )
        self._redundant_bar.get_frame().pack( side="top", padx=3, pady=3 )
        self._redundant_bar.set_title("提示詞多餘率")
        self._lack_bar = number_bar.NumberBar( self._main_frame )
        self._lack_bar.get_frame().pack( side="top", padx=3, pady=3 )
        self._lack_bar.set_title("提示詞缺失率")
    #-------------------------------------------------------------------------
    def get_frame(self):return self._main_frame
    #-------------------------------------------------------------------------
    def set_bar_value(self, score:float, correct_rate:float, redundant_rate:float, lack_rate:float):
        def to_percent(value)->str:
            value = round( value*1e5 )/1e3
            return "{0}%".format( value )
        #..............................................................
        def get_bar_color(value)->str:
            if( value >= 0.8 ):return "#44FF44"
            elif( value >= 0.6 ):return "#77AA44"
            elif( value >= 0.4 ):return "#AA7744"
            elif( value >= 0.2 ):return "#FF4444"
            else:return "#FF0000"
        #...............................................................
        # Score
        if( self._has_score_bar ):
            self._score_bar.set_bar_length_rate( rate=score )
            self._score_bar.set_number( to_percent( score ) )
        # Correct Rate
        bar_color = get_bar_color( correct_rate )
        self._correct_bar.set_bar_length_rate( rate=correct_rate, bar_color=bar_color )
        self._correct_bar.set_number( to_percent( correct_rate ) )
        # Redundant Rate
        bar_color = get_bar_color( 1-redundant_rate )
        self._redundant_bar.set_bar_length_rate( rate=redundant_rate, bar_color=bar_color )
        self._redundant_bar.set_number( to_percent( redundant_rate ) )
        # Lack Rate
        bar_color = get_bar_color( 1-lack_rate )
        self._lack_bar.set_bar_length_rate( rate=lack_rate, bar_color=bar_color )
        self._lack_bar.set_number( to_percent( lack_rate ) )
    #------------------------------------------------------------------------------------------------
    def load_unifier(self, unifier):
        from .. import analysiser
        unifier:analysiser.analysiser_processor.ResultValueUnifier = unifier
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