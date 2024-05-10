
checkpoint_table = {}
checkpoint_list = []
current_checkpoint = None

#-----------------------------------------------------------------
class SDCheckpoint:
    def __init__(self, name:str, title:str):
        self.name = name
        self.title = title
        checkpoint_table[ title ] = self
        checkpoint_list.append(self)
    #-------------------------------------------------------------
    def load(self):
        pass
#=================================================================

def load_checkpoints_table():
    global checkpoint_table, current_checkpoint
    from . import requests
    from . import config_data
    from . import base64
    from . import sleep
    print("載入 Check Point")
    response = requests.get( config_data.sd_checkpoints_url )
    json = response.json()
    if( "detail" in json and json["detail"]=="Not Found" ):
        sleep(1)
        load_checkpoints_table()
        return
    for i in json:
        title = i[ "title" ]
        name = i[ "model_name" ]
        SDCheckpoint( name=name, title=title )
    response = requests.get( config_data.sd_current_checkpoint_url ).json()
    current_checkpoint = checkpoint_table[ response["sd_model_checkpoint"] ]
    print( current_checkpoint.name )
#------------------------------------------------------------------