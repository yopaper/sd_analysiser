from . import os
from . import config_data

tag_list = []

#------------------------------------------------------------------------
def get_all_prompts()->tuple[str]:
    return tuple( tag_list )
#------------------------------------------------------------------------
def has_prompt(prompt:str)->bool:
    prompt = prompt.strip()
    return prompt in tag_list
#-----------------------------------------------------------------------
def create_prompt(prompt:str)->str:
    prompt = prompt.strip()
    if( has_prompt(prompt) ):
        raise Exception( "已存在\"{0}\"的提示詞".format( prompt ) )
    tag_list.append( prompt )
    return prompt
#------------------------------------------------------------------------
def delete_prompt(prompt:str):
    if( not has_prompt( prompt ) ):
        raise Exception( "提示詞:{0} 不存在".format(prompt) )
    tag_list.remove( prompt )
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
        for i in tag_list:
            file_writer.write(i+"\n")
#------------------------------------------------------------------------
load_prompt_data()