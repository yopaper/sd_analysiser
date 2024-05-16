
analysiser_list = []
analysiser_name_table = {}
_init_load_finish = False
#===========================================================================
class AnalysiserCore:
    def __init__(self, name:str):
        from . import analysiser_file
        self.name = name
        self.file_handler = analysiser_file.AnalysiserFile(self)
        analysiser_list.append( self )
        analysiser_name_table[ self.name ] = self
    #-----------------------------------------------------------------------
    def get_name(self)->str:return self.name
    
#===========================================================================
def create_core( name:str )->AnalysiserCore:
    from . import name_checker
    from .. import messagebox
    if( not name_checker.check_name( name ) ):
        messagebox.showerror( title="錯誤名稱", message="輸入的名稱\"{0}\"不可使用!".format(name) )
        return None
    if( name in analysiser_name_table ):
        messagebox.showerror( title="重複名稱", message="輸入的名稱\"{0}\"已被其他模型佔用!".format(name) )
        return None
    if( len( name )<=2 ):
        messagebox.showerror( title="錯誤名稱", message="輸入的名稱\"{0}\"長度過短!".format(name) )
        return None
    AnalysiserCore( name )
#---------------------------------------------------------------------------
def _load_analysiser_list():
    from .. import os, config_data
    global _init_load_finish
    if( _init_load_finish ):return
    if( not os.path.exists( config_data.analysiser_list_file_path ) ):return
    with open( config_data.analysiser_list_file_path, "r" ) as file_reader:
        while(True):
            analysiser_name = file_reader.readline().strip()
            if( len( analysiser_name )<=0 ):break
            AnalysiserCore( analysiser_name )
    _init_load_finish = True
    print("讀取分析模型列表")
#---------------------------------------------------------------------------
def get_all_alalysisers()->tuple[ AnalysiserCore ]:
    _load_analysiser_list()
    return tuple( analysiser_list )
#---------------------------------------------------------------------------
def write_to_file():
    from .. import os, config_data
    if( not os.path.exists( config_data.analysiser_base_path ) ):
        os.makedirs( config_data.analysiser_base_path )
    with open( config_data.analysiser_list_file_path, "w" )as file_writer:
        for ac in get_all_alalysisers():
            file_writer.write( ac.get_name()+"\n" )
#---------------------------------------------------------------------------