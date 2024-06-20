from . import basic_window

class ResultDisplayer:
    def __init__(self, master):
        from . import tk, number_bar, result_number_bar_group
        from .. import config_data
        self.main_frame = tk.LabelFrame( master=master, text="" )

        self.image_canvas = tk.Canvas( self.main_frame, width=config_data.display_image_width, height=config_data.display_image_height )
        self.image_canvas.grid( column=0, row=0, padx=6, pady=6 )
        self.mask_canvas = tk.Canvas( self.main_frame, width=config_data.display_image_width, height=config_data.display_image_height )
        self.mask_canvas.grid( column=1, row=0, padx=6, pady=6 )

        self.bar_group = result_number_bar_group.ResultNumberBarGroup( self.main_frame, has_score_bar=True )
        self.bar_group.get_frame().grid( column=2, row=0, padx=4, pady=4 )

        self.info_label = tk.Label( self.bar_group.get_frame(), text="", wraplength=150 )
        self.info_label.pack( side="top", pady=5 )
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
        
        self.bar_group.load_result( result=result )
        
        info_msg = ""
        if( image.for_test() ):
            info_msg += "<<測試資料>>\n"
        info_msg += "提示詞: {0}\n".format( image.get_prompt() )
        self.info_label.config( text=info_msg )
#========================================================================================================

class AnalysiserViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import analysiser_selection_combobox, result_number_bar_group, scroll_frame, number_bar, page_ui, tk
        from .. import analysiser, prompt_tag

        self._current_processor:analysiser.analysiser_processor.AnalysiserProcessor = None

        super().__init__()
        self.window.title("使用模型")
        self.option_ui_frame = tk.Frame( self.window )
        self.option_ui_frame.grid( column=2, row=0, padx=6, pady=6 )
        frame_height = 750
        # 提示詞數量分析 UI
        self.prompt_number_ui_frame = scroll_frame.ScrollFrame( self.window, text="提示詞數量影響性", width=275, height=frame_height )
        self.prompt_number_ui_frame.grid( column=0, row=0, padx=6, pady=6 )
        self.prompt_number_bar_group_table:dict[ int, result_number_bar_group.ResultNumberBarGroup ] = {}
        for i in range(1, 25):
            bar_group = result_number_bar_group.ResultNumberBarGroup(
                self.prompt_number_ui_frame.get_frame(), title="提示詞數量:{0} 的表現數據".format(i) )
            bar_group.get_frame().pack(side="top", padx=10, pady=4)
            self.prompt_number_bar_group_table[ i ] = bar_group
        self.prompt_number_ui_frame.update_scrollregion()
        # 提示詞影響分析 UI
        self.prompt_group_ui_frame = scroll_frame.ScrollFrame( self.window, text="提示詞彼此影響性", width=275, height=frame_height )
        self.prompt_group_ui_frame.grid( column=1, row=0, padx=6, pady=6 )
        self.prompt_group_bar_group_table:dict[ str, result_number_bar_group.ResultNumberBarGroup ] = {}
        for i in prompt_tag.get_all_prompts():
            bar_group = result_number_bar_group.ResultNumberBarGroup(
                self.prompt_group_ui_frame.get_frame(), title="提示詞 \"{0}\" 存在的影響性".format(i) )
            bar_group.get_frame().pack(side="top", padx=10, pady=4)
            self.prompt_group_bar_group_table[i] = bar_group
        self.prompt_group_ui_frame.update_scrollregion()
        # 模型選擇群組
        self.analysiser_selection_frame = tk.LabelFrame( self.option_ui_frame, text="選擇模型" )
        self.analysiser_selection_frame.grid( column=0, row=0, padx=5, pady=5 )

        self.analysiser_selecter = analysiser_selection_combobox.AnalysiserSelectionCombobox(self.analysiser_selection_frame)
        self.analysiser_selecter.selection_combobox.grid( column=0, row=0, padx=5, pady=5 )
        self.analysiser_selecter.set_on_selected_event( self._update_info_label )

        self.selected_core_info_label = tk.Label( self.analysiser_selection_frame, text="" )
        self.selected_core_info_label.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )

        self.start_process_button = tk.Button( self.analysiser_selection_frame, text="開始分析", command=self._click_to_start_process )
        self.start_process_button.grid( column=1, row=0, padx=5, pady=5 )
        # 頁面群組
        self.page_ui = page_ui.PageUI( self.option_ui_frame )
        self.page_ui.main_frame.grid( column=0, row=1, padx=5, pady=5 )
        self.page_ui.set_max_page_getter( self.get_max_page )
        self.page_ui.set_page_change_event( self._update_displayer_ui )
        # 篩選群組
        self.result_filter_frame = tk.LabelFrame( self.option_ui_frame, text="資料篩選" )
        self.result_filter_frame.grid( column=0, row=2, padx=5, pady=5 )
        self.without_training_data_var = tk.BooleanVar( self.window )
        self.without_training_data_var.set(True)
        self.without_training_data_button = tk.Checkbutton( self.result_filter_frame, text="排除訓練資料", variable=self.without_training_data_var )
        self.without_training_data_button.grid( column=0, row=0, padx=5, pady=5 )
        
        # 整體分析結果
        self.main_result_bar_group = result_number_bar_group.ResultNumberBarGroup( self.option_ui_frame, title="整體分析結果" )
        self.main_result_bar_group.get_frame().grid( column=0, row=3, padx=4, pady=4 )
        # 結果顯示群組
        self.displayer_number = 100
        self.result_display_frame = scroll_frame.ScrollFrame( self.window, text = "圖片個別分析", width=800, height=frame_height )
        self.result_display_frame.grid( column=3, row=0, padx=6, pady=6 )
        self.displayer_list:list[ResultDisplayer] = []
        for i in range( self.displayer_number ):
            displayer = ResultDisplayer( self.result_display_frame.get_frame() )
            self.displayer_list.append( displayer )
            displayer.grid(col=0, row=i)
        self.result_display_frame.update_scrollregion()
        self.window_center()
        self._update_info_label()
    #---------------------------------------------------------------------------------------------------
    def close(self):
        from . import prompt_number_chart_menu
        super().close()
        prompt_number_chart_menu.close_instance()
    #---------------------------------------------------------------------------------------------------
    def get_max_page(self)->int:
        from math import ceil
        if( self._current_processor==None ):return 1
        result_number = len( self._current_processor.get_results() )
        return ceil( result_number / self.displayer_number )
    #---------------------------------------------------------------------------------------------------
    def _click_to_start_process(self)->None:
        from . import messagebox, result_number_bar_group, prompt_number_chart_menu
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
        self.main_result_bar_group.load_unifier( self._current_processor.get_main_unifier() )
        number_key = self._current_processor.get_prompt_number_table_key()
        for i in self.prompt_number_bar_group_table:
            self.prompt_number_bar_group_table[i].reset()
        for i in number_key:
            if( i not in self.prompt_number_bar_group_table ):continue
            self.prompt_number_bar_group_table[i].load_unifier(
                self._current_processor.get_unifiier_with_prompt_number( i ) )
        for i in self.prompt_group_bar_group_table:
            unifier = self._current_processor.get_unifier_with_prompt_group( i )
            bar_group:result_number_bar_group.ResultNumberBarGroup = self.prompt_group_bar_group_table[i]
            if( unifier != None ):
                bar_group.load_unifier(unifier)
            else:bar_group.reset()
        # 顯示圖表
        number_chart_menu = prompt_number_chart_menu.PromptNumberChartMenu()
        number_chart_menu.load_processor( self._current_processor )
        number_chart_menu.open()
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
        self.result_display_frame.update_scrollregion()
#========================================================================================================