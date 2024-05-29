from . import basic_window

class AnalysiserViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import analysiser_selection_combobox, tk
        super().__init__()
        self.window.title("使用模型")
        self.analysiser_selection_frame = tk.LabelFrame( self.window, text="選擇模型" )
        self.analysiser_selection_frame.grid( column=0, row=0, padx=5, pady=5 )

        self.analysiser_selecter = analysiser_selection_combobox.AnalysiserSelectionCombobox(self.analysiser_selection_frame)
        self.analysiser_selecter.selection_combobox.grid( column=0, row=0, padx=5, pady=5 )
        self.analysiser_selecter.set_on_selected_event( self._update_info_label )

        self.selected_core_info_label = tk.Label( self.analysiser_selection_frame, text="" )
        self.selected_core_info_label.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )

        self.start_process_button = tk.Button( self.analysiser_selection_frame, text="開始分析", command=self._click_to_start_process )
        self.start_process_button.grid( column=1, row=0, padx=5, pady=5 )

        self.window_center()
        self._update_info_label()
    #---------------------------------------------------------------------------------------------------
    def _click_to_start_process(self)->None:
        from . import messagebox
        core = self.analysiser_selecter.get_selected_core()
        if( core == None ):
            messagebox.showerror("錯誤", "未選擇模型")
            return
        info = core.get_info()
        info.load_info()
        if( not core.get_info().have_info() ):
            messagebox.showerror("錯誤", "此模型未經訓練")
            return
        processor = core.get_processor()
        processor.start()
    #---------------------------------------------------------------------------------------------------
    def _update_info_label(self, evnet=None)->None:
        core = self.analysiser_selecter.get_selected_core()
        if( core==None ):
            self.selected_core_info_label.config(text="未選擇模型")
            return
        info = core.get_info()
        info.load_info()
        if( not info.have_info() ):
            self.selected_core_info_label.config(text="此模型未訓練過")
            return
        info_msg = ""
        for p in info.get_prompts():
            info_msg += p + ", "
        self.selected_core_info_label.config( text=info_msg )
#========================================================================================================