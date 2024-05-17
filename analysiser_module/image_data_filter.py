
class ImageDataFilter:
    from . import prompt_tag, image_data_handler, checkpoints_loader
    AND_MODE = "and"; OR_MODE = "or"
    def __init__(self, tags:tuple[prompt_tag.PromptTag], checkpoint:checkpoints_loader.SDCheckpoint, mode:str):
        from . import image_data_handler
        self.tags = tuple(tags)
        self.checkpoint = checkpoint
        mode_table = (ImageDataFilter.AND_MODE, ImageDataFilter.OR_MODE)
        assert mode in mode_table, "mode 不可為 {0}".format(mode)
        self.mode = mode
        self._result = []
        self._negative_result = []
        for data in image_data_handler.get_image_datas():
            if( self.checkpoint!=None and self.checkpoint!=data.get_checkpoint() ):continue
            pass_flag = True; negative_flag = True
            if( self.mode == ImageDataFilter.AND_MODE and len( self.tags )!=len( data.get_prompt() ) ):
                pass_flag = False
            for tag in self.tags:
                if( tag.tag() in data.get_prompt() ):
                    negative_flag = False
                else:
                    pass_flag = False
            if( pass_flag ):
                self._result.append( data )
            if( negative_flag ):
                self._negative_result.append( data )
    #---------------------------------------------------------------------------
    def get_result(self)->tuple[ image_data_handler.ImageData ]:
        return tuple( self._result )
    #---------------------------------------------------------------------------
    def get_negative_result(self)->tuple[ image_data_handler.ImageData ]:
        return tuple( self._negative_result )
#===============================================================================