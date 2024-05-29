
analysiser_list = []
analysiser_name_table = {}
_need_to_save = False

#===========================================================================
class AnalysiserCore:
    from . import analysiser_model, analysiser_file, analysiser_info, analysiser_processor
    
    def __init__(self, name:str):
        from . import analysiser_file, analysiser_info, analysiser_processor
        self.name = name
        self.file_handler = analysiser_file.AnalysiserFile( self )
        self.info = analysiser_info.AnalysiserInfo( self )
        self.processor = analysiser_processor.AnalysiserProcessor( self )
        self.model = None
        analysiser_list.append( self )
        analysiser_name_table[ self.name ] = self
    #-----------------------------------------------------------------------
    def get_info( self )->analysiser_info.AnalysiserInfo:
        return self.info
    #-----------------------------------------------------------------------
    def get_file_handler(self)->analysiser_file.AnalysiserFile:
        return self.file_handler
    #-----------------------------------------------------------------------
    def get_name(self)->str:return self.name
    #-----------------------------------------------------------------------
    def get_processor(self)->analysiser_processor.AnalysiserProcessor:
        return self.processor
    #-----------------------------------------------------------------------
    def get_model(self)->analysiser_model.ImageAnalysiser:
        from . import analysiser_model
        if( self.model == None ):
            self.model = analysiser_model.ImageAnalysiser()
        return self.model
    #-----------------------------------------------------------------------
    def free_model(self)->None:
        self.model = None
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
    global _need_to_save
    if(_need_to_save):return
    _need_to_save = True
    if( not os.path.exists( config_data.analysiser_list_file_path ) ):return
    with open( config_data.analysiser_list_file_path, "r" ) as file_reader:
        while(True):
            analysiser_name = file_reader.readline().strip()
            if( len( analysiser_name )<=0 ):break
            AnalysiserCore( analysiser_name )
    print("讀取分析模型列表")
#---------------------------------------------------------------------------
def get_all_alalysisers()->tuple[ AnalysiserCore ]:
    _load_analysiser_list()
    return tuple( analysiser_list )
#---------------------------------------------------------------------------
def get_core_with_name(name:str)->AnalysiserCore:
    if( name in analysiser_name_table ):
        return analysiser_name_table[name]
    return None
#---------------------------------------------------------------------------
def write_to_file():
    global _need_to_save
    from .. import os, config_data
    if( not os.path.exists( config_data.analysiser_base_path ) ):
        os.makedirs( config_data.analysiser_base_path )
    if( not _need_to_save ):return
    print("Save Core List")
    with open( config_data.analysiser_list_file_path, "w" )as file_writer:
        for ac in get_all_alalysisers():
            file_writer.write( ac.get_name()+"\n" )
#---------------------------------------------------------------------------