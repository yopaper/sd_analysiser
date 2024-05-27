
from . import requests
from . import json
from . import base64
from . import config_data
from . import sleep
from . import Thread
from . import tkui
from . import os
from . import json
#--------------------------------------------------------------
"""
import urllib.request
result = urllib.request.urlopen( "http://127.0.0.1:7860/" )
"""

checkpoints_model_table = ()

#-------------------------------------------------------------
def txt_to_image( prompt:str, negative_prompt:str="", seed:int=None, step:int=20 ):
    from random import randint
    from sys import maxsize
    from . import info_key
    from . import checkpoints_loader
    info = {}
    info[info_key.PROMPT_KEY] = prompt
    # negative_prompt
    info[info_key.NEGATIVE_KEY] = negative_prompt
    # seed
    if(seed!=None):info[info_key.SEED_KEY] = seed
    else:info[info_key.SEED_KEY] = randint(0, maxsize)
    # step
    info[info_key.STEP_KEY] = step
    info_str = json.dumps(info)

    info[ info_key.CHECK_POINT_KEY ] = checkpoints_loader.get_current_checkpoint().title
    
    response = requests.post( url=config_data.sd_txt2img_api_url, data=info_str ).json()
    response = response["images"][0]
    response = base64.b64decode( response )
    return response, info
#--------------------------------------------------------------
def check_sd_enable(wait_sec:float=1.2)->bool:
    import urllib.request
    try:
        result = urllib.request.urlopen( config_data.sd_url )
        return True
    except:
        return False
#--------------------------------------------------------------
def open_sd():
    def run_command():
        print("Stable Diffusion not working, activate it...")
        os.system("python ../sd_web/webui/launch.py --api")
        print("Stable Diffusion End")
    #...........................................................
    if( check_sd_enable() ):return
    t = Thread( target=run_command )
    t.daemon = True
    t.start()
    tkui.wait_sd_window.WaitSDWindow().open()
    print("Stable Diffusion Open!")
#--------------------------------------------------------------