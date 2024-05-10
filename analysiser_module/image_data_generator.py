
class PromptTagArranger:
    def __init__(self, arrange_prompts, fix_prompts=None, max_number:int=None):
        from . import item_arranger
        self.arrange_prompts = tuple( arrange_prompts )
        self.fix_prompts = ()
        if( fix_prompts!=None ):
            self.fix_prompts += tuple(fix_prompts)
        self.arranger = item_arranger.ItemArranger(self.arrange_prompts, 0)
        self.end = False
        self.current_number = 0
        self.max_number = 0
        if( max_number != None ):self.max_number += max_number
        else:self.max_number += len( arrange_prompts )
    #------------------------------------------------------------------------
    def next(self):
        from . import item_arranger
        if(self.end):return
        self.arranger.next()
        if( self.arranger.is_end() ):
            self.current_number += 1
            if( self.current_number > self.max_number ):
                self.end = True
                return
            self.arranger = item_arranger.ItemArranger( self.arrange_prompts, self.current_number )
    #-------------------------------------------------------------------------
    def get_prompts(self):
        assert self.end != True, "此PromptTagArranger已經到盡頭"
        return self.fix_prompts + self.arranger.get_item()
    #---------------------------------------------------------------------------
    def get_prompts_str(self)->str:
        prompt_str = ""
        prompts = self.get_prompts()
        for i in prompts:
            prompt_str += i + ", "
        if( len( prompt_str )>0 ):
            return prompt_str[0:-2]
        return prompt_str
    #---------------------------------------------------------------------------
    def is_end(self):
        return self.end
#===============================================================================

class ImageDataGenerator:
    def __init__(self, tag_arranger:PromptTagArranger, image_number:int=250):
        self.tag_arranger = tag_arranger
        self.image_number = image_number
    #----------------------------------------------------------------------------
    def start(self):
        from . import api_handler
        from . import image_data_handler
        print("開始生成圖片")
        while( not self.tag_arranger.is_end() ):
            prompt_str = self.tag_arranger.get_prompts_str()
            self.tag_arranger.next()
            if( len(prompt_str)<=0 ):continue
            for i in range(self.image_number):
                image, info = api_handler.txt_to_image( prompt=prompt_str )
                image_data_handler.save_image_data( image=image, image_info=info )
        print("生成結束")
#================================================================================