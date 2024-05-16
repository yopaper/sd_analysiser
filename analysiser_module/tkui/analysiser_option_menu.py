from . import basic_window
from . import tk, ttk

class AnalysiserOptionMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import filter_ui
        from .. import prompt_tag, analysiser
        super().__init__()
        self.window.title("分析模型")

        self.analysiser_manager_frame = tk.LabelFrame( self.window, text="管理" )
        self.analysiser_manager_frame.grid( column=0, row=0, padx=6, pady=6 )
        tk.Label( self.analysiser_manager_frame, text="選擇分析模型" ).grid(column=0, row=0, padx=5, pady=5)
        prompt_list = [p.get_name() for p in analysiser.analysiser_core.get_all_alalysisers()]
        self.analysiser_selection_combobox = ttk.Combobox( self.analysiser_manager_frame, values=prompt_list, state="readonly" )
        self.analysiser_selection_combobox.grid( column=1, row=0, padx=5, pady=5 )
        # 管理按鈕列
        self.button_row_frame = tk.Frame( self.analysiser_manager_frame )
        self.button_row_frame.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )
        self.create_analysiser_button = tk.Button( self.button_row_frame, text=" 建 立 模 型 ", command=self._click_to_create_analysiser )
        self.create_analysiser_button.grid( column=0, row=0, padx=5, pady=5 )
        self.rename_analysiser_button = tk.Button( self.button_row_frame, text="從新命名" )
        self.rename_analysiser_button.grid( column=1, row=0, padx=5, pady=5 )
        self.delete_analysiser_button = tk.Button( self.button_row_frame, text="刪除模型" )
        self.delete_analysiser_button.grid( column=2, row=0, padx=5, pady=5 )

        # 模型訓練UI
        self.train_ui_frame = tk.LabelFrame( self.window, text="訓練" )
        self.train_ui_frame.grid(row=1, column=0, padx=6, pady=6)
        tk.Label( self.train_ui_frame, text="訓練Epoch" ).grid(column=0, row=0, padx=4, pady=4)
        self.train_epoch_spinbox = tk.Spinbox( self.train_ui_frame, from_=1, to=890604 )
        self.train_epoch_spinbox.grid( column=1, row=0, padx=6, pady=6 )

        self.train_data_filter_frame = tk.LabelFrame(self.train_ui_frame, text="訓練資料篩選")
        self.train_data_filter_frame.grid( column=0, row=1, columnspan=2, padx=6, pady=6 )

        self.data_filter_ui = filter_ui.FullFilterUI( self.train_data_filter_frame )
        self.data_filter_ui.grid( column=0, row=0 )

        self.data_filter_ui.update()
        self.window_center()
    #---------------------------------------------------------------------------
    def _click_to_create_analysiser(self):
        from .. import simpledialog, analysiser
        intput_name = simpledialog.askstring(title="建立新分析模型", prompt="輸入模型名稱")
        if( intput_name==None ):return
        analysiser.analysiser_core.create_core( intput_name )
        self.analysiser_selection_combobox.config( values=[ ac.get_name() for ac in analysiser.analysiser_core.get_all_alalysisers() ] )
#===============================================================================