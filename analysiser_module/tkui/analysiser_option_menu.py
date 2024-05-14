from . import basic_window
from . import tk, ttk

class AnalysiserOptionMenu(basic_window.BasicWindow):
    def __init__(self):
        from .. import prompt_tag
        super().__init__()
        self.window.title("分析模型")

        self.prompt_selection_frame = tk.Frame( self.window )
        self.prompt_selection_frame.grid( column=0, row=0 )
        tk.Label( self.prompt_selection_frame, text="選擇提示詞" ).grid(column=0, row=0)
        prompt_list = [p.tag() for p in prompt_tag.get_all_prompts()]
        self.selection_combobox = ttk.Combobox( self.prompt_selection_frame, values=prompt_list, state="readonly" )
        self.selection_combobox.grid( column=1, row=0 )

        # 模型訓練UI
        self.train_ui_frame = tk.LabelFrame( self.window, text="訓練" )
        self.train_ui_frame.grid(row=1, column=0)
        tk.Label( self.train_ui_frame, text="訓練Epoch" ).grid(column=0, row=0)
        self.train_epoch_spinbox = tk.Spinbox( self.train_ui_frame, from_=1, to=890604 )
        self.train_epoch_spinbox.grid( column=1, row=0 )

        self.train_data_filter_mode_frame = tk.LabelFrame(self.train_ui_frame, text="訓練資料篩選")
        self.train_data_filter_mode_frame.grid( column=0, row=1, columnspan=2 )
        self.and_mode_button = tk.Radiobutton( self.train_data_filter_mode_frame, text="僅有特定提示詞" )
        self.and_mode_button.grid( column=0, row=0 )
        self.or_mode_button = tk.Radiobutton( self.train_data_filter_mode_frame, text="包含特定提示詞" )
        self.or_mode_button.grid( column=1, row=0 )

        self.window_center()
#===============================================================================