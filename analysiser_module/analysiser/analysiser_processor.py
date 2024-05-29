

class AnalysiserProcessor:
    def __init__(self, core):
        from . import analysiser_core
        self._core:analysiser_core.AnalysiserCore = core
    #-------------------------------------------------------------------
    def start(self)->None:
        from . import torch
        from .. import image_data_handler
        
        print("開始分析")
        print("模型載入權重")
        model = self._core.get_model()
        model.load_weight()
        model.eval()
        #...............................................................
        def process_image_data(image_data:image_data_handler.ImageData):
            print( "分析:{0}".format(image_data.file_name) )
            tensor_data = image_data.get_tensor_data()
            output = model( tensor_data )
            mean_value = torch.mean( output )
            print( mean_value )
        #...............................................................
        image_datas = image_data_handler.get_image_datas()
        for img in image_datas:
            process_image_data( img )
#=======================================================================