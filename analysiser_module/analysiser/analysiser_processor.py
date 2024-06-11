

class AnalysiserProcessor:
    def __init__(self, core, without_training_data:bool=True):
        from . import analysiser_core, process_result
        self._core:analysiser_core.AnalysiserCore = core
        self._result_list:list[ process_result.ProcessResult ] = []
        self._without_training_data = without_training_data
        self._avg_correct_rate:float = 0
        self._avg_redundant_rate:float = 0
        self._avg_lack_rate:float = 0
        self._prompt_number_score={}
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
            if( self._without_training_data and self._core.get_info().trained_with_data( image_data ) ):return
            print( "分析:{0}".format(image_data.file_name) )
            tensor_data = image_data.get_tensor_data()
            #print( tensor_data.mean() )
            output = model( tensor_data )
            result = process_result.ProcessResult( core=self._core, image_data=image_data, model_out=output )
            self._avg_correct_rate += result.get_correct_rate()
            self._avg_redundant_rate += result.get_redundant_rate()
            self._avg_lack_rate += result.get_lack_rate()
            self._result_list.append( result )
        #...............................................................
        image_datas = image_data_handler.get_image_datas()
        for img in image_datas:
            process_image_data( img )
        result_number = len( self._result_list )
        self._avg_correct_rate /= result_number
        self._avg_redundant_rate /= result_number
        self._avg_lack_rate /= result_number

    #-------------------------------------------------------------------
    def get_avg_correct_rate(self)->float:return self._avg_correct_rate
    def get_avg_redundant_rate(self)->float:return self._avg_redundant_rate
    def get_avg_lack_rate(self)->float:return self._avg_lack_rate
    #-------------------------------------------------------------------
    def get_results(self):
        return tuple( self._result_list )
#=======================================================================