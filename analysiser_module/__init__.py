import importlib
import os
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
import requests
import base64
import json

from threading import Thread
from time import sleep
from PIL import Image, ImageTk

from . import config_data
from . import tkui
from . import api_handler
from . import prompt_tag
from . import checkpoints_loader
from . import image_data_handler
from . import image_data_filter
from . import info_key
from . import image_data_generator
from . import item_arranger

from . import analysiser
#-------------------------------------------------------------
def main():
    def loading_function():
        api_handler.open_sd()
        checkpoints_loader.load_checkpoints_table()
        image_data_handler.load_image_datas()
    tkui.main_menu.get_instance().window.after( 1, loading_function )
    tkui.main_menu.get_instance().open()

    prompt_tag.write_to_file()
    analysiser.analysiser_core.write_to_file()
#--------------------------------------------------------------
main()