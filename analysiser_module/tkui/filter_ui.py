from . import tk


#=====================================================================================
class PromptFilterUI:
    from .. import prompt_tag

    def __init__(self, master):
        from .. import prompt_tag, image_data_filter
        self.enable_prompts = []
        self.master = master

        self.main_frame = tk.LabelFrame( master, text="提示詞篩選" )
        self.prompt_filter_listbox = tk.Listbox( self.main_frame, selectmode=tk.SINGLE )
        self.prompt_filter_listbox.grid( column=0, row=0, padx=6, pady=6 )
        self.prompt_filter_listbox.bind("<<ListboxSelect>>", self.on_listbox_selected)
        for prompt in prompt_tag.get_all_prompts():
            self.prompt_filter_listbox.insert( "end", "－ "+prompt.tag() )

        self.filter_mode_var = tk.StringVar( self.main_frame )
        self.filter_mode_frame = tk.LabelFrame( self.main_frame, text="篩選原則" )
        self.filter_mode_frame.grid( column=0, row=1, padx=6, pady=6 )
        self.and_mode_button = tk.Radiobutton(
            self.filter_mode_frame, text="僅有特定提示詞", command=lambda:self.on_click(),
            value=image_data_filter.ImageDataFilter.AND_MODE, variable=self.filter_mode_var )
        self.and_mode_button.grid( column=0, row=0, padx=8 )
        self.or_mode_button = tk.Radiobutton(
            self.filter_mode_frame, text="包含特定提示詞", command=lambda:self.on_click(),
            value=image_data_filter.ImageDataFilter.OR_MODE, variable=self.filter_mode_var )
        self.or_mode_button.grid( column=0, row=1, padx=8 )
        self.filter_mode_var.set( image_data_filter.ImageDataFilter.OR_MODE )

        self.enable_prompts_frame = tk.LabelFrame( self.main_frame, text="已選擇提示詞" )
        self.enable_prompts_frame.grid( column=0, row=2, padx=6, pady=6 )
        self.enable_prompts_label = tk.Label( self.enable_prompts_frame, wraplength=200 )
        self.enable_prompts_label.grid( column=0, row=2, padx=4, pady=4 )

        self.on_click = None
    #---------------------------------------------------------------------------------
    def get_enable_prompts(self)->tuple[prompt_tag.PromptTag]:
        return tuple( self.enable_prompts )
    #---------------------------------------------------------------------------------
    def get_filter_mode(self)->str:
        return self.filter_mode_var.get()
    #---------------------------------------------------------------------------------
    def grid( self, column:int, row:int ):
        self.main_frame.grid( column=column, row=row, padx=6, pady=6 )
    #---------------------------------------------------------------------------------
    def on_listbox_selected(self, evt=None):
        from .. import prompt_tag, image_data_filter
        selection = self.prompt_filter_listbox.curselection()
        if( len( selection )<=0 ):return
        selection = selection[0]
        prompt = prompt_tag.get_all_prompts()[selection]
        # 更新 listbox
        self.prompt_filter_listbox.insert("end", "19890604")
        self.prompt_filter_listbox.delete( selection )
        if( prompt in self.enable_prompts ):
            self.enable_prompts.remove( prompt )
            self.prompt_filter_listbox.insert( selection, "－ "+prompt.tag() )
        else:
            self.enable_prompts.append( prompt )
            self.prompt_filter_listbox.insert( selection, "● "+prompt.tag() )
        self.prompt_filter_listbox.delete("end")
        # 更新 label
        msg = ""
        for p in self.get_enable_prompts():
            msg += "●" + p.tag() + " "
        self.enable_prompts_label.config( text=msg )
        if( self.on_click!=None ):
            self.on_click()
#=====================================================================================
class CheckpointFilterUI:
    from .. import checkpoints_loader
    NULL_SELECTION = "# 不選擇 #"
    def __init__(self, master, have_null:bool=True):
        from . import ttk
        from .. import checkpoints_loader
        self.master = master

        self.main_frame = tk.LabelFrame( master, text="Checkpoint篩選" )
        selection_list = [cp.name for cp in checkpoints_loader.get_all_chechpoints()]
        if( have_null ):selection_list.insert( 0, CheckpointFilterUI.NULL_SELECTION )
        self.selection_combobox = ttk.Combobox(
            self.main_frame, values=selection_list, state="readonly" )
        self.selection_combobox.set( checkpoints_loader.get_current_checkpoint().name )
        self.selection_combobox.grid( column=0, row=0, padx=8, pady=8 )
        self.selection_combobox.bind( "<<ComboboxSelected>>", self.on_select )
        
        self.on_click = None
    #----------------------------------------------------------------------------------
    def on_select(self, event):
        print( self.selection_combobox.get() )
        if( self.on_click!=None ):self.on_click()
    #----------------------------------------------------------------------------------
    def get_selected_chechpoint(self)->checkpoints_loader.SDCheckpoint:
        from .. import checkpoints_loader
        selected_name = self.selection_combobox.get()
        if( selected_name != CheckpointFilterUI.NULL_SELECTION ):
            return checkpoints_loader.get_with_name( selected_name )
        return None
    #----------------------------------------------------------------------------------
    def grid(self, column:int, row:int):
        self.main_frame.grid( column=column, row=row, padx=8, pady=8 )
#======================================================================================
class FullFilterUI:
    from .. import image_data_filter
    def __init__(self, master):
        self.master = master
        self.main_frame = tk.Frame( self.master )
        self.data_number_label = tk.Label( self.main_frame, text="" )
        self.data_number_label.grid( column=0 ,row=0 )
        self.prompts_ui = PromptFilterUI( self.main_frame )
        self.prompts_ui.grid( column=0, row=1 )
        self.prompts_ui.on_click = self.update
        self.checkpoint_ui = CheckpointFilterUI( self.main_frame )
        self.checkpoint_ui.grid( column=0, row=2 )
        self.checkpoint_ui.on_click = self.update
        self.on_click = None
        self.current_filter = None
    #-----------------------------------------------------------------------------------
    def grid( self, column:int, row:int ):
        self.main_frame.grid( column=column, row=row )
    #-----------------------------------------------------------------------------------
    def get_filter(self)->image_data_filter.ImageDataFilter:
        if( self.current_filter == None ):self.update()
        return self.current_filter
    #-----------------------------------------------------------------------------------
    def update(self):
        from .. import image_data_filter
        self.current_filter = image_data_filter.ImageDataFilter(
            tags = self.prompts_ui.get_enable_prompts(),
            checkpoint = self.checkpoint_ui.get_selected_chechpoint(),
            mode = self.prompts_ui.get_filter_mode()
        )
        data_number = len(self.current_filter.get_result())
        self.data_number_label.config( text="符合圖片數量:{0}".format(data_number) )
        if( self.on_click!=None ):self.on_click()
    #-----------------------------------------------------------------------------------
    def set_click_event( self, event ):
        self.on_click = event
#=======================================================================================