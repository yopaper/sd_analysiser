from . import tk
from . import basic_window

class PromptManagerMenu(basic_window.BasicWindow):
    def __init__(self):
        super().__init__()
        self.window.title( "提示詞管理" )
        # ListBox
        self.prompt_listbox = tk.Listbox(master=self.window)
        self.prompt_listbox.grid(row=0, column=0, rowspan=5)
        self.prompt_listbox.bind("<<ListboxSelect>>", self.on_select_list)
        self.update_prompt_list()

        self.exit_button = tk.Button(self.window, text="返回", command=self.close)
        self.exit_button.grid(row=0, column=1)
        # 新增區 .......................................................................
        self.new_prompt_tag = tk.StringVar()
        self.create_prompt_frame = tk.LabelFrame(self.window, text="新增")
        self.create_prompt_frame.grid(row=1, column=1)
        self.prompt_input = tk.Entry(self.create_prompt_frame, textvariable=self.new_prompt_tag)
        self.prompt_input.grid(column=0, row=0)
        self.create_new_prompt_button = tk.Button(self.create_prompt_frame, text="新增提示詞", command=self.add_new_prompt)
        self.create_new_prompt_button.grid( column=0, row=1 )
        # 管理區 .......................................................................
        self.selected_prompt = None
        self.manage_prompt_frame = tk.LabelFrame(self.window, text="管理")
        self.manage_prompt_frame.grid(row=2, column=1)
        self.selection_label = tk.Label(self.manage_prompt_frame, text="未選擇提示詞")
        self.selection_label.grid(column=0, row=0)
        self.delete_prompt_button = tk.Button(self.manage_prompt_frame, text="刪除提示詞", command=self.delete_selected_prompt)
        self.delete_prompt_button.grid(column=0, row=1)

        self.window_center()
    #-------------------------------------------------------------------------------------
    def add_new_prompt(self):
        from .. import prompt_tag
        from . import messagebox
        prompt = self.new_prompt_tag.get()
        if( len( prompt )<=0 ):return
        try:prompt_tag.create_prompt( prompt )
        except Exception as e:
            messagebox.showerror(title="錯誤", message=e)
        self.update_prompt_list()
    #-------------------------------------------------------------------------------------
    def delete_selected_prompt(self):
        from .. import prompt_tag
        if( self.selected_prompt==None ):return
        prompt_tag.delete_prompt( self.selected_prompt )
        self.selected_prompt = None
        self.update_prompt_list()
    #-------------------------------------------------------------------------------------
    def on_select_list(self, event):
        selection = self.prompt_listbox.curselection()
        if( len(selection)<=0 ):return
        selection = self.prompt_listbox.get( selection[0] )
        self.selected_prompt = selection
        self.selection_label.config( text="選擇提示詞<{0}>".format(self.selected_prompt) )
    #-------------------------------------------------------------------------------------
    def update_prompt_list(self):
        from .. import prompt_tag
        self.prompt_listbox.delete(0, 'end')
        for i in prompt_tag.get_all_prompts():
            self.prompt_listbox.insert(0, i)
#=========================================================================================