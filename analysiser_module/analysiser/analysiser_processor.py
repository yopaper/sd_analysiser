
class ResultValueUnifier:
    def __init__(self):
        self._result_number:int = 0
        self._correct_rate_sum:float = 0
        self._redundant_rate_sum:float = 0
        self._lack_rate_sum:float = 0
    #-------------------------------------------------------------------
    def add_result(self, result):
        from . import process_result
        result:process_result.ProcessResult = result
        self._result_number += 1
        self._correct_rate_sum += result.get_correct_rate()
        self._redundant_rate_sum += result.get_redundant_rate()
        self._lack_rate_sum += result.get_lack_rate()
    #--------------------------------------------------------------------
    def get_avg_correct_rate(self)->float:
        return self._correct_rate_sum / self._result_number
    #--------------------------------------------------------------------
    def get_avg_redundant_rate(self)->float:
        return self._redundant_rate_sum / self._result_number
    #--------------------------------------------------------------------
    def get_avg_lack_rate(self)->float:
        return self._lack_rate_sum / self._result_number
#========================================================================
class AnalysiserProcessor:
    def __init__(self, core, without_training_data:bool=True):
        from . import analysiser_core, process_result
        self._core:analysiser_core.AnalysiserCore = core
        self._result_list:list[ process_result.ProcessResult ] = []
        self._without_training_data = without_training_data
        self._main_unifier = ResultValueUnifier()
        self._prompt_number_unifier:dict[ int, ResultValueUnifier ] = {}
    #-------------------------------------------------------------------
    def start(self)->None:
        from . import torch, process_result
        from .. import image_data_handler
        
        print("開始分析")
        model = self._core.get_model()
        model.load_weight()
        model.eval()
        self._result_list.clear()
        #...............................................................
        def process_image_data(image_data:image_data_handler.ImageData):
            # 檢測排除訓練資料
            if( self._without_training_data and self._core.get_info().trained_with_data( image_data ) ):return
            print( "分析:{0}".format(image_data.file_name) )
            tensor_data = image_data.get_tensor_data()
            #print( tensor_data.mean() )
            output = model( tensor_data )
            result = process_result.ProcessResult( core=self._core, image_data=image_data, model_out=output )
            self._main_unifier.add_result( result )
            prompt_number:int = len( image_data.get_prompt() )
            if( prompt_number not in self._prompt_number_unifier ):
                self._prompt_number_unifier[ prompt_number ] = ResultValueUnifier()
            self._prompt_number_unifier[ prompt_number ].add_result( result )
            self._result_list.append( result )
        #...............................................................
        image_datas = image_data_handler.get_image_datas()
        for img in image_datas:
            process_image_data( img )
    #-------------------------------------------------------------------
    def get_main_unifier(self):return self._main_unifier
    def get_avg_correct_rate(self)->float:return self._main_unifier.get_avg_correct_rate()
    def get_avg_redundant_rate(self)->float:return self._main_unifier.get_avg_redundant_rate()
    def get_avg_lack_rate(self)->float:return self._main_unifier.get_avg_lack_rate()
    #-------------------------------------------------------------------
    def get_prompt_number_table_key(self)->tuple[int]:
        table_key = [pn for pn in self._prompt_number_unifier]
        for i in range( len( table_key ) ):
            for j in range( i, len( table_key ) ):
                a = table_key[i]; b = table_key[j]
                if( a > b ):
                    table_key[j] = a
                    table_key[i] = b
        return tuple( table_key )
    #-------------------------------------------------------------------
    def get_unifiier_with_prompt_number(self, prompt_number:int):
        if( prompt_number not in self._prompt_number_unifier ):return None
        unifier:ResultValueUnifier = self._prompt_number_unifier[ prompt_number ]
        return unifier
    #-------------------------------------------------------------------
    def get_results(self):
        return tuple( self._result_list )
#=======================================================================