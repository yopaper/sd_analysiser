
class AnalysiserInfo:
    def __init__(self, core):
        from . import analysiser_core
        self._core:analysiser_core.AnalysiserCore = core
        self._info_dict = {}
        self._info_loaded = False
    #-----------------------------------------------------------------------
    def get_info_dict(self)->dict:return self._info_dict
    #-----------------------------------------------------------------------
    def load_info(self)->None:
        from .. import json, os
        file_path = self._core.file_handler.get_info_file_path()
        if( not os.path.exists( file_path ) ):return
        with open( file_path, "r" )as file_reader:
            json_table = json.load( file_reader )
            for key in json_table:
                self._info_dict[key] = json_table[key]
        self._info_loaded = True
    #-----------------------------------------------------------------------
    def get_info_with_key(self, key:str):
        if( key in self._info_dict ):
            return self._info_dict[key]
        return None
    #-----------------------------------------------------------------------
    def get_checkpoint(self):
        from .. import checkpoints_loader, info_key
        checkpoint_name = self.get_info_with_key(info_key.CHECK_POINT_KEY)
        if( checkpoint_name==None ):return None
        return checkpoints_loader.get_with_name( checkpoint_name )
    #-----------------------------------------------------------------------
    def get_epoch(self)->int:
        from .. import info_key
        return self.get_info_with_key( info_key.EPOCH_KEY )
    #-----------------------------------------------------------------------
    def get_learning_rate(self)->float:
        from .. import info_key
        return self.get_info_with_key( info_key.LEARNING_RATE_KEY )
    #-----------------------------------------------------------------------
    def get_batch_size(self)->int:
        from .. import info_key
        return self.get_info_with_key( info_key.BATCH_SIZE_KEY )
    #-----------------------------------------------------------------------
    def get_min_train_loss(self)->float:
        from .. import info_key
        return self.get_info_with_key( info_key.MIN_TRAIN_LOSS_KEY )
    #-----------------------------------------------------------------------
    def get_prompts(self)->tuple[ str ]:
        from .. import info_key
        prompt_list = self.get_info_with_key( info_key.PROMPT_KEY )
        if( prompt_list != None ):
            return tuple( prompt_list )
        return None
    #-----------------------------------------------------------------------
    def get_training_data_name_list(self)->tuple[ str ]:
        from .. import info_key
        data_list = self.get_info_with_key( info_key.TRAIN_DATA_NAME_LIST )
        if( data_list != None ):return tuple( data_list )
        return ()
    #-----------------------------------------------------------------------
    def trained_with_data(self, image_data)->bool:
        from .. import image_data_handler
        training_data_list = self.get_training_data_name_list()
        image_data:image_data_handler.ImageData = image_data
        return image_data.get_name() in training_data_list
    #-----------------------------------------------------------------------
    def compare_imagedata_prompt(self, image_data)->bool:
        from .. import image_data_handler
        image_data:image_data_handler.ImageData = image_data
        core_prompts = self.get_prompts()
        image_prompts = image_data.get_prompt()
        for p in core_prompts:
            if( p not in image_prompts ):
                return False
        return True
    #-----------------------------------------------------------------------
    def have_info(self)->bool:return self._info_loaded
#=============================================================================