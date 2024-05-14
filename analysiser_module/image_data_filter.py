
class ImageDataFilter:
    from . import prompt_tag, image_data_handler
    AND_MODE = "and"; OR_MODE = "or"
    def __init__(self, tags:tuple[prompt_tag.PromptTag], mode:str):
        from . import image_data_handler
        self.tags = tuple(tags)
        mode_table = (ImageDataFilter.AND_MODE, ImageDataFilter.OR_MODE)
        assert mode in mode_table, "mode 不可為 {0}".format(mode)
        self.mode = mode
        self.result = []
        for data in image_data_handler.get_image_datas():
            if( self.mode == ImageDataFilter.AND_MODE and len( self.tags )!=len( data.get_prompt() ) ):continue
            pass_flag = True
            for tag in self.tags:
                if( tag.tag() not in data.get_prompt() ):
                    pass_flag = False
                    break
            if( pass_flag ):
                self.result.append( data )
    #---------------------------------------------------------------------------
    def get_result(self)->tuple[ image_data_handler.ImageData ]:
        return tuple( self.result )
#===============================================================================