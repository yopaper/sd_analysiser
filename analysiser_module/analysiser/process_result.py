
class ProcessResult:
    from . import torchvision
    to_pil_transform = torchvision.transforms.ToPILImage()

    def __init__(self, core, image_data, model_out) -> None:
        from . import analysiser_core, torch, torchvision
        from .. import image_data_handler, ImageTk, Image

        model_out:torch.Tensor = model_out.squeeze( dim=0 ).squeeze( dim=0 )
        self._core:analysiser_core.AnalysiserCore = core
        self._image_data:image_data_handler.ImageData = image_data
        self._predicted_score = float( torch.mean( model_out ) )
        self._image_positive = self._core.get_info().compare_imagedata_prompt( image_data )

        # 正確率
        self._correct_rate:float
        # 多餘率
        self._redundant_rate:float
        # 缺失率
        self._lack_rate:float

        if( self._image_positive ):
            self._correct_rate = self._predicted_score
            self._redundant_rate = None
            self._lack_rate = 1 - self._predicted_score
        else:
            self._correct_rate = 1 - self._predicted_score
            self._redundant_rate = self._predicted_score
            self._lack_rate = None
            
        # 虛擬特徵圖
        max_value = model_out.max(); min_value = model_out.min()
        value_delta = max_value - min_value
        r_ch = 1 - (model_out - min_value)/value_delta
        g_ch = (model_out - min_value)/value_delta
        b_ch = torch.zeros_like( model_out )
        color_mask = torch.stack( (r_ch, g_ch, b_ch), dim=0 )
        original_size_mask:Image.Image = ProcessResult.to_pil_transform( color_mask )
        original_size_mask = original_size_mask.resize( (self._image_data.get_tk_image().width(), self._image_data.get_tk_image().height() ) )
        self._predicted_mask_pil = original_size_mask.resize( (self._image_data.get_tk_image().width(), self._image_data.get_tk_image().height() ) )
        original_size_mask.close()
        self._predicted_mask_tkpil : ImageTk = ImageTk.PhotoImage( self._predicted_mask_pil )
        
    #-----------------------------------------------------------------
    def free(self):
        self._predicted_mask_pil.close()
        del self._core
        del self._image_data
        del self._predicted_score
        del self._image_positive
        del self._predicted_mask_tkpil
    #-----------------------------------------------------------------
    def get_correct_rate(self)->float:
        return self._correct_rate
    #-----------------------------------------------------------------
    def get_redundant_rate(self)->float:return self._redundant_rate
    #-----------------------------------------------------------------
    def get_lack_rate(self)->float:return self._lack_rate
    #-----------------------------------------------------------------
    def get_score(self)->float:
        return self._predicted_score
    #-----------------------------------------------------------------
    def get_predicted_mask(self):
        return self._predicted_mask_tkpil
    #-----------------------------------------------------------------
    def get_image_data(self):
        return self._image_data
#=====================================================================