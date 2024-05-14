
image_data_list = []

#================================================================================
class ImageData:
    from . import ImageTk, Image
    def __init__(self, file_name:str):
        from . import config_data
        self.file_name = file_name
        self.image_file_path = get_image_file_path( file_name )
        self.image_info_path = get_image_info_path( file_name )
        self.tk_image = None
        self.image_info = None
        self.prompt_table = None
        image_data_list.append( self )
    #-----------------------------------------------------------------------------
    def get_prompt(self)->tuple[str]:
        from . import prompt_key
        if( self.prompt_table==None ):
            prompt_str = self.get_info()[ prompt_key.PROMPT_KEY ]
            prompt_split = prompt_str.split(",")
            self.prompt_table = [ p.strip() for p in prompt_split ]
        return tuple( self.prompt_table )
    #-----------------------------------------------------------------------------
    def get_info(self)->dict:
        from . import json
        if( self.image_info==None ):
            with open( self.image_info_path ) as file_reader:
                self.image_info = json.load( file_reader )
        return self.image_info
    #-----------------------------------------------------------------------------
    def get_tk_image(self)->ImageTk:
        from . import Image, ImageTk, config_data
        if( self.tk_image==None ):
            pil_image = Image.open( self.image_file_path )
            wh_rate = pil_image.width / pil_image.height
            # 若寬度較大
            if( wh_rate > config_data.display_image_wh_rate ):
                size_rate = config_data.display_image_width / pil_image.width
                pil_image = pil_image.resize( ( round( pil_image.width*size_rate), round(pil_image.height*size_rate) ) )
            # 若高度較大
            else:
                size_rate = config_data.display_image_height / pil_image.height
                pil_image = pil_image.resize( ( round( pil_image.width*size_rate), round(pil_image.height*size_rate) ) )
            self.tk_image = ImageTk.PhotoImage( pil_image )
        return self.tk_image

#=================================================================================

image_data_file_counter = 1

#---------------------------------------------------------------------------------
def get_image_info_path(file_name:str):
    from . import config_data
    return config_data.image_info_path + file_name + ".txt"
#---------------------------------------------------------------------------------
def get_image_file_path(file_name:str):
    from . import config_data
    return config_data.image_file_path + file_name + ".png"
#---------------------------------------------------------------------------------
def save_image_data(image, image_info:dict, file_name:str=None):
    from . import json
    if( file_name==None ):
        file_name = get_counter_file_name()
    image_file_path = get_image_file_path( file_name )
    image_info_path = get_image_info_path( file_name )
    with open( image_file_path, "wb" )as file_writer:
        file_writer.write( image )
    with open( image_info_path, "w" )as file_writer:
        file_writer.write( json.dumps( image_info ) )
    ImageData( file_name )
#---------------------------------------------------------------------------------
def get_counter_file_name()->str:
    from . import os
    global image_data_file_counter
    while( True ):
        name = str( image_data_file_counter ).zfill( 10 )
        file_path = get_image_file_path( name )
        if( not os.path.exists( file_path ) ):
            return name
        image_data_file_counter += 1
#---------------------------------------------------------------------------------
def get_image_datas()->tuple[ ImageData ]:
    return tuple( image_data_list )
#---------------------------------------------------------------------------------
def load_image_datas():
    from . import os, config_data
    print("讀取圖片資料")
    if( not os.path.exists( config_data.image_file_path ) ):
        os.makedirs( config_data.image_file_path )
    if( not os.path.exists( config_data.image_info_path ) ):
        os.makedirs( config_data.image_info_path )
    file_list = os.listdir( config_data.image_file_path )
    for file_name in file_list:
        main_file_name = file_name.split(".")[0]
        ImageData( main_file_name )
#---------------------------------------------------------------------------------