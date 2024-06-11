from . import tk
from . import basic_window

class ImageGeneratorMenu(basic_window.BasicWindow):
    DISABLED = 0; FIX = 1; ARRANGE = 2

    def __init__(self):
        super().__init__()
        self.selected_prompt = None
        self.enable_fix_prompts = []
        self.enable_arranged_prompts = []

        self.window.title("圖片生成")

        tk.Label( self.window, text="未啟用提示詞" ).grid( column=0, row=1 )
        tk.Label( self.window, text="固定提示詞" ).grid( column=1, row=1 )
        tk.Label( self.window, text="排序提示詞" ).grid( column=2, row=1 )
        tk.Label( self.window, text="排列組合預覽" ).grid( column=3, row=1 )
        # Prompt Button
        self.disabled_button = tk.Button(self.window, text="設為不啟用", command=lambda target_list=None:self.set_selection_to_list(target_list))
        self.disabled_button.grid( column=0, row=0 )
        self.fix_button = tk.Button(self.window, text="設為固定", command=lambda target_list=self.enable_fix_prompts:self.set_selection_to_list(target_list))
        self.fix_button.grid( column=1, row=0 )
        self.arranged_button = tk.Button(self.window, text="設為排序", command=lambda target_list=self.enable_arranged_prompts:self.set_selection_to_list(target_list))
        self.arranged_button.grid( column=2, row=0 )

        # Prompt Listbox
        list_box_rowspan = 8
        self.disabled_prompt_listbox = tk.Listbox(self.window, width=15)
        self.disabled_prompt_listbox.grid( column=0, row=2, rowspan=list_box_rowspan )
        self.bind_listbox_select( self.disabled_prompt_listbox )

        self.fix_prompt_listbox = tk.Listbox(self.window, width=15)
        self.fix_prompt_listbox.grid( column=1, row=2, rowspan=list_box_rowspan )
        self.bind_listbox_select( self.fix_prompt_listbox )

        self.arranged_prompt_listbox = tk.Listbox(self.window, width=15)
        self.arranged_prompt_listbox.grid( column=2, row=2, rowspan=list_box_rowspan )
        self.bind_listbox_select( self.arranged_prompt_listbox )

        self.demo_prompt_listbox = tk.Listbox(self.window, width=40)
        self.demo_prompt_listbox.grid( column=3, row=2, rowspan=list_box_rowspan )

        # 右側UI
        self.exit_button = tk.Button( self.window, text="返回", command=self.close )
        self.exit_button.grid( column=6, row=0 )

        self.start_generate_button = tk.Button( self.window, text="開始生成", command=self.start_generate_image )
        self.start_generate_button.grid( column=4, row=2 )
        tk.Label( self.window, text="圖片生成量" ).grid( column=4, row=3 )
        self.image_number_box = tk.Spinbox( self.window, from_=1, to=896400 )
        self.image_number_box.grid( column=5, row=3 )

        self.prompt_update()
        self.window_center()
    #-------------------------------------------------------------------------------------
    def set_selection_to_list(self, target_list:list):
        if( self.selected_prompt == None ):return
        if( self.selected_prompt in self.enable_arranged_prompts ):
            self.enable_arranged_prompts.remove( self.selected_prompt )
        if( self.selected_prompt in self.enable_fix_prompts ):
            self.enable_fix_prompts.remove( self.selected_prompt )
        if( target_list!=None ):
            target_list.append( self.selected_prompt )
        self.prompt_update()
    #-------------------------------------------------------------------------------------
    # 將一個 Listbox 綁定上選擇事件
    def bind_listbox_select(self, listbox):
        def select_function(env):
            listbox_select = listbox.curselection()
            if( len(listbox_select)<=0 ):return
            select_index = listbox_select[0]
            self.selected_prompt = listbox.get( select_index )
            print( "選擇:{0}".format(self.selected_prompt) )
        listbox.bind( "<<ListboxSelect>>", select_function )
    #-------------------------------------------------------------------------------------
    def start_generate_image(self):
        from .. import image_data_generator
        image_number = 0
        try:image_number += int(self.image_number_box.get())
        except Exception as e:
            print(e)
            return
        tag_arranger = image_data_generator.PromptTagArranger(self.enable_arranged_prompts, self.enable_fix_prompts)
        image_generator = image_data_generator.ImageDataGenerator( tag_arranger=tag_arranger, image_number=image_number )
        image_generator.start()
    #-------------------------------------------------------------------------------------
    def prompt_update(self):
        from .. import prompt_tag
        from .. import image_data_generator
        self.disabled_prompt_listbox.delete(0, "end")
        self.fix_prompt_listbox.delete(0, "end")
        self.arranged_prompt_listbox.delete(0, "end")
        self.demo_prompt_listbox.delete(0, "end")

        for i in prompt_tag.get_all_prompts():
            current_tag = i
            if( current_tag in self.enable_fix_prompts ):
                self.fix_prompt_listbox.insert( 0, current_tag )
            elif( current_tag in self.enable_arranged_prompts ):
                self.arranged_prompt_listbox.insert( 0, current_tag )
            else:
                self.disabled_prompt_listbox.insert( 0, current_tag )
        
        tag_arranger = image_data_generator.PromptTagArranger(self.enable_arranged_prompts, self.enable_fix_prompts)
        i=0
        while( not tag_arranger.is_end() ):
            current_tag_str = tag_arranger.get_prompts_str()
            print( current_tag_str )
            self.demo_prompt_listbox.insert( 0, "({0}):{1}".format(i, current_tag_str) )
            i += 1
            tag_arranger.next()
#=========================================================================================