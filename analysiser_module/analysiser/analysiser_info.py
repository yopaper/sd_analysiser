
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
    def have_info(self)->bool:return self._info_loaded
#=============================================================================