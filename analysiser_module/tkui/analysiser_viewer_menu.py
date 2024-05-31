from . import basic_window

class ResultDisplayer:
    def __init__(self, master):
        from . import tk
        from .. import config_data
        self.main_frame = tk.LabelFrame( master=master, text="" )
        self.canvas = tk.Canvas( self.main_frame, width=config_data.display_image_width, height=config_data.display_image_height )
        self.canvas.grid( column=0, row=0, padx=6, pady=6 )
        self.info_label = tk.Label( self.main_frame, text="", wraplength=150 )
        self.info_label.grid( column=1, row=0 )
    #----------------------------------------------------------------------------------------------------
    def grid(self, col:int, row:int):
        self.main_frame.grid( column=col, row=row, padx=8, pady=8 )
    #----------------------------------------------------------------------------------------------------
    def _reset_displayer(self):
        self.canvas.delete("all")
        self.main_frame.config( text="" )
        self.info_label.config( text="" )
    #----------------------------------------------------------------------------------------------------
    def load_result(self, result):
        from .. import analysiser
        self._reset_displayer()
        if( result==None ):return
        result:analysiser.process_result.ProcessResult = result
        self.canvas.create_image( (0, 0), anchor = "nw", image = result.get_image_data().get_tk_image() )
        self.main_frame.config( text=result.get_image_data().file_name )
        info_msg = ""
        score = round(result.get_score() * 1e8) / 1e6
        info_msg += "分析結果: {0}%\n".format( score )
        info_msg += "提示詞: {0}\n".format( result.get_image_data().get_prompt() )
        self.info_label.config( text=info_msg )
#========================================================================================================

class AnalysiserViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import analysiser_selection_combobox, page_ui, tk
        from .. import analysiser

        self._current_processor:analysiser.analysiser_processor.AnalysiserProcessor = None

        super().__init__()
        self.window.title("使用模型")

        self.left_ui_frame = tk.Frame( self.window )
        self.left_ui_frame.grid( column=0, row=0, padx=6, pady=6 )
        # 模型選擇群組
        self.analysiser_selection_frame = tk.LabelFrame( self.left_ui_frame, text="選擇模型" )
        self.analysiser_selection_frame.grid( column=0, row=0, padx=5, pady=5 )

        self.analysiser_selecter = analysiser_selection_combobox.AnalysiserSelectionCombobox(self.analysiser_selection_frame)
        self.analysiser_selecter.selection_combobox.grid( column=0, row=0, padx=5, pady=5 )
        self.analysiser_selecter.set_on_selected_event( self._update_info_label )

        self.selected_core_info_label = tk.Label( self.analysiser_selection_frame, text="" )
        self.selected_core_info_label.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )

        self.start_process_button = tk.Button( self.analysiser_selection_frame, text="開始分析", command=self._click_to_start_process )
        self.start_process_button.grid( column=1, row=0, padx=5, pady=5 )
        # 頁面群組
        self.page_ui = page_ui.PageUI( self.left_ui_frame )
        self.page_ui.main_frame.grid( column=0, row=1, padx=5, pady=5 )
        self.page_ui.set_max_page_getter( self.get_max_page )
        self.page_ui.set_page_change_event( self._update_displayer_ui )
        # 結果顯示群組
        self.displayer_width = 3; self.displayer_height = 2
        self.displayer_number = self.displayer_width * self.displayer_height
        self.result_display_group = tk.LabelFrame( self.window, text = "圖片個別分析" )
        self.result_display_group.grid( column=1, row=0, padx=8, pady=8 )
        self.displayer_list:list[ResultDisplayer] = []
        for y in range( self.displayer_height ):
            for x in range( self.displayer_width ):
                displayer = ResultDisplayer( self.result_display_group )
                self.displayer_list.append( displayer )
                displayer.grid( col=x, row=y )

        self.window_center()
        self._update_info_label()
    #---------------------------------------------------------------------------------------------------
    def get_max_page(self)->int:
        from math import ceil
        if( self._current_processor==None ):return 1
        result_number = len( self._current_processor.get_results() )
        return ceil( result_number / self.displayer_number )
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
        self._current_processor = core.get_processor()
        self._current_processor.start()
        self._update_displayer_ui()
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
    #----------------------------------------------------------------------------------------------------
    def _update_displayer_ui(self):
        if( self._current_processor==None ):return
        results = self._current_processor.get_results()
        def single_displayer(i:int):
            current_displayer = self.displayer_list[i]
            result_index = self.page_ui.get_current_page()*self.displayer_number + i
            if( result_index >= len( results ) ):return
            current_result = results[result_index]
            current_displayer.load_result( current_result )
        #................................................................................................
        for i in range( self.displayer_number ):
            single_displayer( i )
#========================================================================================================