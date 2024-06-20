
class AnalysiserProcessor:
    def __init__(self, core, without_training_data:bool=True):
        from . import analysiser_core, process_result, result_value_unifier
        self._core:analysiser_core.AnalysiserCore = core
        self._result_list:list[ process_result.ProcessResult ] = []
        self._without_training_data = without_training_data
        self._main_unifier = result_value_unifier.ResultValueUnifier()
        self._prompt_number_unifier:dict[ int, result_value_unifier.ResultValueUnifier ] = {}
        self._prompt_group_unifier:dict[ str, result_value_unifier.ResultValueUnifier ] = {}
    #-------------------------------------------------------------------
    def start(self)->None:
        from . import process_result, result_value_unifier
        from .. import image_data_handler
        from random import random
        print("開始分析")
        model = self._core.get_model().cuda()
        model.load_weight()
        model.eval()
        self._result_list.clear()
        #...............................................................
        def process_image_data(image_data:image_data_handler.ImageData):
            # 檢測排除訓練資料
            if( self._without_training_data and self._core.get_info().trained_with_data( image_data ) ):return
            print( "分析:{0}".format(image_data.file_name) )
            tensor_data = image_data.get_tensor_data()
            output = model( tensor_data )
            result = process_result.ProcessResult( core=self._core, image_data=image_data, model_out=output )
            self._result_list.append( result )
            self._main_unifier.add_result( result )
            # 處理提示詞數量
            prompt_number:int = len( image_data.get_prompt() )
            if( prompt_number not in self._prompt_number_unifier ):
                self._prompt_number_unifier[ prompt_number ] = result_value_unifier.ResultValueUnifier()
            self._prompt_number_unifier[ prompt_number ].add_result( result )
            # 處理個別提示詞
            prompts = image_data.get_prompt()
            for prompt in prompts:
                if( prompt not in self._prompt_group_unifier ):
                    self._prompt_group_unifier[prompt] = result_value_unifier.ResultValueUnifier()
                self._prompt_group_unifier[prompt].add_result( result=result )
        #...............................................................
        image_datas = image_data_handler.get_image_datas()
        for img in image_datas:
            ##if( random()<=0.965 ):continue
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
        from . import result_value_unifier
        if( prompt_number not in self._prompt_number_unifier ):return None
        unifier:result_value_unifier.ResultValueUnifier = self._prompt_number_unifier[ prompt_number ]
        return unifier
    #-------------------------------------------------------------------
    def get_unifier_with_prompt_group(self, prompt:str):
        from . import result_value_unifier
        if( prompt not in self._prompt_group_unifier ):return None
        unifier:result_value_unifier.ResultValueUnifier = self._prompt_group_unifier[ prompt ]
        return unifier
    #-------------------------------------------------------------------
    def get_results(self):
        return tuple( self._result_list )
#=======================================================================