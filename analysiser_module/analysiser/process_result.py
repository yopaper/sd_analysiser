
class ProcessResult:
    def __init__(self, core, image_data, model_out) -> None:
        from . import analysiser_core, torch
        from .. import image_data_handler

        model_out:torch.Tensor = model_out
        self._core:analysiser_core.AnalysiserCore = core
        self._image_data:image_data_handler.ImageData = image_data
        self._predicted_score = float( torch.mean( model_out ) )
    #-----------------------------------------------------------------
    def get_score(self)->float:
        return self._predicted_score
    #-----------------------------------------------------------------
    def get_image_data(self):
        return self._image_data
#=====================================================================