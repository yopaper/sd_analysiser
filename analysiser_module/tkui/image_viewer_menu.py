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
        #print("載入:"+image_data.file_name)
        self.image_data = image_data
        info_dict = image_data.get_info()
        info_str = ""
        info_str += "●檔案名稱:\n{0}\n".format( image_data.file_name )
        if( prompt_key.PROMPT_KEY in info_dict ):
            info_str += "●提示詞:\n{0}\n".format( info_dict[ prompt_key.PROMPT_KEY ] )
        if( prompt_key.SEED_KEY in info_dict ):
            info_str += "●種子:\n{0}\n".format( info_dict[ prompt_key.SEED_KEY ] )
        self.info_label.config(text=info_str)
        #print("開始繪製")
        self.canvas.create_image( (0, 0), anchor="nw", image=image_data.get_tk_image() )
    #---------------------------------------------------------------------------------
#=====================================================================================
class FilterUI:
    def __init__(self, menu):
        from .. import prompt_tag
        self.enable_prompts = []
        self.menu = menu

        self.filter_ui_frame = tk.LabelFrame( menu.left_ui_group, text="圖片篩選" )
        tk.Label( self.filter_ui_frame, text="提示詞篩選" ).grid( column=0, row=0 )
        self.prompt_filter_listbox = tk.Listbox( self.filter_ui_frame, selectmode=tk.SINGLE )
        self.prompt_filter_listbox.grid( column=0, row=1 )
        self.prompt_filter_listbox.bind("<<ListboxSelect>>", self.on_listbox_selected)

        for prompt in prompt_tag.get_all_prompts():
            self.prompt_filter_listbox.insert( "end", "－ "+prompt.tag() )
    #---------------------------------------------------------------------------------
    def on_listbox_selected(self, evt):
        from .. import prompt_tag, image_data_filter
        selection = self.prompt_filter_listbox.curselection()
        if( len( selection )<=0 ):return
        selection = selection[0]
        prompt = prompt_tag.get_all_prompts()[selection]

        self.prompt_filter_listbox.insert("end", "19890604")
        self.prompt_filter_listbox.delete( selection )
        if( prompt in self.enable_prompts ):
            self.enable_prompts.remove( prompt )
            
            self.prompt_filter_listbox.insert( selection, "－ "+prompt.tag() )
        else:
            self.enable_prompts.append( prompt )
            self.prompt_filter_listbox.insert( selection, "● "+prompt.tag() )
            
        self.prompt_filter_listbox.delete("end")

        data_filter = image_data_filter.ImageDataFilter( self.enable_prompts, mode=image_data_filter.ImageDataFilter.OR_MODE )
        self.menu.set_images_to_show( data_filter.get_result() )
    #---------------------------------------------------------------------------------

#=====================================================================================

class ImageViewerMenu(basic_window.BasicWindow):
    from .. import image_data_handler
    def __init__(self):
        from .. import image_data_handler
        super().__init__()
        self.window.title("圖片資料瀏覽")
        self.image_to_show = image_data_handler.get_image_datas()

        self.left_ui_group = tk.Frame(self.window)
        self.left_ui_group.grid( column=0, row=1 )

        self.filter_ui = FilterUI( self )
        self.filter_ui.filter_ui_frame.grid( column=0, row=1 )
        
        self.exit_button = tk.Button( self.window, text=" 返回 ", command=self.close )
        self.exit_button.grid( column=2, row=0 )
        # 頁面切換UI
        self.page_ui_group = tk.LabelFrame( self.left_ui_group, text="頁面" )
        self.page_ui_group.grid( column=0, row=0 )
        # 上一頁
        self.last_page_button = tk.Button( self.page_ui_group, text="上一頁", command=lambda delta=-1:self.change_page(delta) )
        self.last_page_button.grid( column=0, row=0 )
        self.page_label = tk.Label( self.page_ui_group, text="" )
        self.page_label.grid( column=1, row=0 )
        # 下一頁
        self.next_page_button = tk.Button( self.page_ui_group, text="下一頁", command=lambda delta=1:self.change_page(delta) )
        self.next_page_button.grid( column=2, row=0 )

        self.page = 0
        image_group_width = 4; image_group_height = 4
        self.displayer_number = image_group_width * image_group_height
        # 圖片展示群組
        self.image_group = tk.LabelFrame( self.window, text="圖片" )
        self.image_group.grid( column=1, row=1, rowspan=1 )
        self.displayer_list = []
        for y in range(image_group_height):
            for x in range( image_group_width ):
                displayer = ImageDisplayer( self.image_group )
                displayer.displayer_group.grid( column=x, row=y )
                self.displayer_list.append( displayer )
        
        self.window_center(200)
        self.change_page(0)
    #-------------------------------------------------------------------------------------
    def set_images_to_show(self, images_to_show:tuple[image_data_handler.ImageData]):
        self.image_to_show = images_to_show
        self.change_page(0)
    #-------------------------------------------------------------------------------------
    def change_page(self, delta:int):
        from math import ceil
        max_page = ceil( len( self.image_to_show )/self.displayer_number )
        if( max_page<=0 ):max_page = 1
        self.page += delta
        if( self.page < 0 ):self.page = max_page-1
        if( self.page >= max_page ):self.page = 0
        self.page_label.config( text="{0}/{1}".format(self.page+1, max_page) )
        self.update_image_ui()
    #--------------------------------------------------------------------------------------
    def update_image_ui(self):
        from .. import image_data_handler
        i = self.page * self.displayer_number
        for ui in self.displayer_list:
            if( i >= len( self.image_to_show ) ):
                ui.reset()
            else:
                ui.load_image_data( self.image_to_show[i] )
            i += 1
#=========================================================================================