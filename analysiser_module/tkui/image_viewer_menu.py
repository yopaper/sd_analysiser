from . import tk
from . import basic_window

class ImageDisplayer:
    from .. import image_data_handler
    def __init__(self, master):
        from .. import config_data
        self.displayer_group = tk.Frame(master)
        self.canvas = tk.Canvas( self.displayer_group, width=config_data.display_image_width, height=config_data.display_image_height )
        self.info_label = tk.Label( self.displayer_group, text="" )
        self.info_button = tk.Label( self.displayer_group, text="資訊" )
        self.canvas.grid(row=0, column=0)
        self.info_label.grid(row=0, column=1)
        self.image_data = None
    #---------------------------------------------------------------------------------
    def reset(self):
        self.image_data = None
        self.canvas.delete("all")
        self.info_label.config(text="")
    #---------------------------------------------------------------------------------
    def load_image_data(self, image_data:image_data_handler.ImageData):
        from .. import prompt_key
        self.reset()
        if( image_data==None ):return
        print("載入:"+image_data.file_name)
        self.image_data = image_data
        info_dict = image_data.get_info()
        info_str = ""
        info_str += "●檔案名稱:\n{0}\n".format( image_data.file_name )
        if( prompt_key.PROMPT_KEY in info_dict ):
            info_str += "●提示詞:\n{0}\n".format( info_dict[ prompt_key.PROMPT_KEY ] )
        if( prompt_key.SEED_KEY in info_dict ):
            info_str += "●種子:\n{0}\n".format( info_dict[ prompt_key.SEED_KEY ] )
        self.info_label.config(text=info_str)
        print("開始繪製")
        self.canvas.create_image( (0, 0), anchor="nw", image=image_data.get_tk_image() )
    #---------------------------------------------------------------------------------

#=====================================================================================
class ImageViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        super().__init__()
        self.window.title("圖片資料瀏覽")

        self.left_ui_group = tk.Frame(self.window)
        self.left_ui_group.grid( column=0, row=1 )

        tk.Label( self.left_ui_group, text="提示詞篩選" ).grid( column=0, row=0 )
        self.prompt_filter_listbox = tk.Listbox( self.left_ui_group )
        self.prompt_filter_listbox.grid( column=0, row=1 )

        self.image_group = tk.LabelFrame( self.window, text="圖片" )
        self.image_group.grid( column=1, row=1, rowspan=1 )
        self.displayer_list = []
        self.exit_button = tk.Button( self.window, text="返回", command=self.close )
        self.exit_button.grid( column=2, row=0 )

        self.page_ui_group = tk.LabelFrame( self.window, text="頁面" )
        self.page_ui_group.grid( column=1, row=0 )
        self.last_page_button = tk.Button( self.page_ui_group, text="上一頁" )
        self.last_page_button.grid( column=0, row=0 )
        self.page_label = tk.Label( self.page_ui_group, text="" )
        self.page_label.grid( column=1, row=0 )
        self.next_page_button = tk.Button( self.page_ui_group, text="下一頁" )
        self.next_page_button.grid( column=2, row=0 )

        image_group_width = 5; image_group_height = 4
        self.displayer_number = image_group_width * image_group_height

        for y in range(image_group_height):
            for x in range( image_group_width ):
                displayer = ImageDisplayer( self.image_group )
                displayer.displayer_group.grid( column=x, row=y )
                self.displayer_list.append( displayer )
        
        self.window_center(200)
        self.update_image_ui()
    #-------------------------------------------------------------------------------------
    def update_image_ui(self):
        from .. import image_data_handler
        i = 0
        for ui in self.displayer_list:
            if( i >= len(image_data_handler.image_data_list) ):
                ui.reset()
            else:
                ui.load_image_data(image_data_handler.image_data_list[i])
            i += 1
#=========================================================================================