
class AnalysiserFile:
    from . import analysiser_core
    def __init__(self, core:analysiser_core.AnalysiserCore) -> None:
        from .. import config_data
        self.core = core
        self._base_path = config_data.analysiser_base_path + self.core.get_name() + "/"
        self._info_file_path = self._base_path + "analysiser_info.json"
    #------------------------------------------------------------------
    def get_base_path(self)->str:
        _check_and_create_path( self._base_path )
        return self._base_path
    #------------------------------------------------------------------
    def get_info_file_path(self)->str:
        _check_and_create_path( self._base_path )
        return self._info_file_path
#======================================================================
def _check_and_create_path(path:str):
    from .. import os
    if( os.path.exists( path ) ):return
    os.makedirs(path)
#----------------------------------------------------------------------