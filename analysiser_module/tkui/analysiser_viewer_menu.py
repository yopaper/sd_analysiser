from . import basic_window

class ResultDisplayer:
    def __init__(self, master):
        from . import tk, number_bar
        from .. import config_data
        self.main_frame = tk.LabelFrame( master=master, text="" )

        self.image_canvas = tk.Canvas( self.main_frame, width=config_data.display_image_width, height=config_data.display_image_height )
        self.image_canvas.grid( column=0, row=0, padx=6, pady=6 )
        self.mask_canvas = tk.Canvas( self.main_frame, width=config_data.display_image_width, height=config_data.display_image_height )
        self.mask_canvas.grid( column=1, row=0, padx=6, pady=6 )

        self.right_ui_frame = tk.Frame( self.main_frame )
        self.right_ui_frame.grid( column=2, row=0, padx=4, pady=4 )

        self.score_bar = number_bar.NumberBar( self.right_ui_frame )
        self.score_bar.grid( column=0, row=0 )
        self.correct_bar = number_bar.NumberBar( self.right_ui_frame )
        self.correct_bar.grid( column=0, row=1 )

        self.info_label = tk.Label( self.right_ui_frame, text="", wraplength=150 )
        self.info_label.grid( column=0, row=2 )
    #----------------------------------------------------------------------------------------------------
    def grid(self, col:int, row:int):
        self.main_frame.grid( column=col, row=row, padx=8, pady=8 )
    #----------------------------------------------------------------------------------------------------
    def _reset_displayer(self):
        self.image_canvas.delete("all")
        self.mask_canvas.delete("all")
        self.main_frame.config( text="" )
        self.info_label.config( text="" )
    #----------------------------------------------------------------------------------------------------
    def load_result(self, result):
        from .. import analysiser
        self._reset_displayer()
        if( result==None ):return
        result:analysiser.process_result.ProcessResult = result
        image = result.get_image_data()
        self.image_canvas.create_image( (0, 0), anchor = "nw", image = result.get_image_data().get_tk_image() )
        self.mask_canvas.create_image( (0, 0), anchor = "nw", image = result.get_predicted_mask() )
        self.main_frame.config( text=result.get_image_data().file_name )
        
        self.score_bar.set_bar_length_rate( rate=result.get_score() )
        score = round(result.get_score() * 1e5) / 1e3
        self.score_bar.set_title( "分析結果" )
        self.score_bar.set_number( score )

        correct_rate = result.get_correct_rate()
        bar_color:str
        if( correct_rate >= 0.666 ):bar_color = "#22FF22"
        elif( correct_rate >= 0.333 ):bar_color = "#AAAA33"
        else:bar_color = "#FF2222"
        self.correct_bar.set_bar_length_rate( rate=correct_rate, bar_color=bar_color )
        correct_rate = round(correct_rate * 1e5) / 1e3
        self.correct_bar.set_title("提示詞正確率")
        self.correct_bar.set_number( correct_rate )
        
        info_msg = ""
        if( image.for_test() ):
            info_msg += "<<測試資料>>\n"
        info_msg += "提示詞: {0}\n".format( image.get_prompt() )
        self.info_label.config( text=info_msg )
#========================================================================================================

class AnalysiserViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import analysiser_selection_combobox, scroll_frame, number_bar, page_ui, tk
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
        # 篩選群組
        self.result_filter_frame = tk.LabelFrame( self.left_ui_frame, text="資料篩選" )
        self.result_filter_frame.grid( column=0, row=2, padx=5, pady=5 )
        self.without_training_data_var = tk.BooleanVar( self.window )
        self.without_training_data_var.set(True)
        self.without_training_data_button = tk.Checkbutton( self.result_filter_frame, text="排除訓練資料", variable=self.without_training_data_var )
        self.without_training_data_button.grid( column=0, row=0, padx=5, pady=5 )
        
        # 整體分析結果
        self.main_result_frame = tk.LabelFrame( self.left_ui_frame, text="整體分析結果" )
        self.main_result_frame.grid( column=0, row=3, padx=5, pady=5 )
        self.correct_rate_bar = number_bar.NumberBar( self.main_result_frame, width=130 )
        self.correct_rate_bar.grid( column=0, row=0 )
        self.correct_rate_bar.set_title( "平均提示詞正確率" )
        self.correct_rate_bar.set_bar_length_rate(rate=0)
        self.correct_rate_bar.set_number( "未分析" )
        self.redundant_rate_bar = number_bar.NumberBar( self.main_result_frame, width=130 )
        self.redundant_rate_bar.grid( column=0, row=1 )
        self.redundant_rate_bar.set_title( title="平均提示詞多餘率" )
        self.redundant_rate_bar.set_bar_length_rate(rate=0)
        self.redundant_rate_bar.set_number( "未分析" )
        self.lack_rate_bar = number_bar.NumberBar( self.main_result_frame, width=130 )
        self.lack_rate_bar.grid( column=0, row=2 )
        self.lack_rate_bar.set_title( title="平均提示詞缺失率" )
        self.lack_rate_bar.set_bar_length_rate(rate=0)
        self.lack_rate_bar.set_number( "未分析" )
        # 測試
        self.mf = tk.Frame( self.left_ui_frame )
        self.mf.grid( column=0, row=4 )
        self.c = tk.Canvas( self.mf, width=200, height=200 )
        self.c.pack( side="left" )
        self.sb = tk.Scrollbar( self.mf )
        self.sb.pack( side="right", fill="y" )
        self.f = tk.Frame( self.c )
        self.c.create_window( (0, 0), window=self.f, anchor="nw" )
        for i in range(20):
            tk.Label( self.f, text="Label:{0}".format( i ) ).grid( column=0, row=i )
        self.c.yview_moveto(0.2)
        # 結果顯示群組
        self.displayer_width = 2; self.displayer_height = 3
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
        from .. import analysiser
        core = self.analysiser_selecter.get_selected_core()
        if( core == None ):
            messagebox.showerror("錯誤", "未選擇模型")
            return
        info = core.get_info()
        info.load_info()
        if( not core.get_info().have_info() ):
            messagebox.showerror("錯誤", "此模型未經訓練")
            return
        # 分析處理器
        self._current_processor = analysiser.analysiser_processor.AnalysiserProcessor(
            core=core, without_training_data=self.without_training_data_var.get() )
        self._current_processor.start()
        # 更新UI
        self._update_displayer_ui()
        correct_rate = self._current_processor.get_avg_correct_rate()
        bar_color:str
        if( correct_rate >= 0.666 ):bar_color = "#11FF11"
        elif( correct_rate >= 0.333 ):bar_color = "#AAAA22"
        else:bar_color = "#FF1111"
        self.correct_rate_bar.set_bar_length_rate( rate=correct_rate, bar_color=bar_color )
        correct_rate = round( correct_rate*1e5 )/1e3
        self.correct_rate_bar.set_number( correct_rate )

        redundant_rate = self._current_processor.get_avg_redundant_rate()
        self.redundant_rate_bar.set_bar_length_rate( rate=redundant_rate )
        redundant_rate = round( redundant_rate*1e5 ) / 1e3
        self.redundant_rate_bar.set_number( redundant_rate )

        lack_rate = self._current_processor.get_avg_lack_rate()
        self.lack_rate_bar.set_bar_length_rate( rate=lack_rate )
        lack_rate = round( lack_rate*1e5 ) / 1e3
        self.lack_rate_bar.set_number( lack_rate )
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