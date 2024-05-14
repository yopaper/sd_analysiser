from . import os
from . import config_data

tag_table = {}
tag_list = []

class PromptTag:
    
    def __init__(self, prompt:str) -> None:
        self.prompt = prompt
        tag_table[ self.prompt ] = self
        tag_list.append( self )
    #------------------------------------------------------
    def tag(self)->str:
        return self.prompt
    #------------------------------------------------------
    
#=======================================================================

def get_all_prompts()->tuple[PromptTag]:
    return tuple( tag_list )
#------------------------------------------------------------------------
def has_prompt(prompt:str)->bool:
    prompt = prompt.strip()
    return prompt in tag_table
#-----------------------------------------------------------------------
def create_prompt(prompt:str)->PromptTag:
    prompt = prompt.strip()
    if( has_prompt(prompt) ):
        raise Exception( "已存在\"{0}\"的提示詞".format( prompt ) )
    return PromptTag( prompt )
#------------------------------------------------------------------------
def delete_prompt(prompt:str):
    if( not has_prompt( prompt ) ):
        raise Exception( "提示詞:{0} 不存在".format(prompt) )
    del tag_table[ prompt ]
#------------------------------------------------------------------------
def load_prompt_data():
    print("讀取提示詞檔案")
    if( not os.path.exists(config_data.prompt_data_path) ):return
    with open( config_data.prompt_data_path, "r" )as file_reader:
        while(True):
            line = file_reader.readline()
            if( line==None or len( line )<=0 ):break
            line = line.strip()
            create_prompt( line )
#------------------------------------------------------------------------
def write_to_file():
    if( not os.path.exists( config_data.data_base_path ) ):
        os.makedirs( config_data.data_base_path )
    with open( config_data.prompt_data_path, "w" )as file_writer:
        for i in tag_table:
            file_writer.write(i+"\n")
#------------------------------------------------------------------------
load_prompt_data()