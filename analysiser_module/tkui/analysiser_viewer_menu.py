from . import tk, basic_window

class ResultDisplayer(tk.LabelFrame):
    def __init__(self, master):
        from . import tk, number_bar, result_number_bar_group
        from .. import config_data
        super().__init__(master=master, text="")

        self.image_canvas = tk.Canvas( self, width=config_data.display_image_width, height=config_data.display_image_height )
        self.image_canvas.grid( column=0, row=0, padx=6, pady=6 )
        self.mask_canvas = tk.Canvas( self, width=config_data.display_image_width, height=config_data.display_image_height )
        self.mask_canvas.grid( column=1, row=0, padx=6, pady=6 )

        self.bar_group = result_number_bar_group.ResultNumberBarGroup( self, has_score_bar=True )
        self.bar_group.get_frame().grid( column=2, row=0, padx=4, pady=4 )

        self.info_label = tk.Label( self.bar_group.get_frame(), text="", wraplength=150 )
        self.info_label.pack( side="top", pady=5 )
    #----------------------------------------------------------------------------------------------------
    def reset_displayer(self):
        self.image_canvas.delete("all")
        self.mask_canvas.delete("all")
        self.info_label.config( text="" )
    #----------------------------------------------------------------------------------------------------
    def load_result(self, result):
        from .. import analysiser
        self.reset_displayer()
        if( result==None ):return
        result:analysiser.process_result.ProcessResult = result
        image = result.get_image_data()
        self.image_canvas.create_image( (0, 0), anchor = "nw", image = result.get_image_data().get_tk_image() )
        mask = result.get_predicted_mask()
        if( mask != None ):
            self.mask_canvas.create_image( (0, 0), anchor = "nw", image = mask )
        self.config( text=result.get_image_data().file_name )
        
        self.bar_group.load_result( result=result )
        
        info_msg = ""
        info_msg += "Prompt: {0}\n".format( image.get_prompt() )
        self.info_label.config( text=info_msg )
#========================================================================================================
class DisplayerFrame( tk.Frame ):
    def __init__(self, master):
        from . import page_ui
        from .. import analysiser
        super().__init__( master=master )
        top_frame = tk.Frame( self )
        top_frame.pack( side="top" )
        tk.Label( top_frame, text="Result of Single Image" ).pack(side="left")
        self._page_ui = page_ui.PageUI( top_frame )
        self._page_ui.main_frame.pack( side="left" )
        self._displayer_number = 50
        self._displayers_list:list[ ResultDisplayer ] = []
        self._loaded_results:list[ list[ analysiser.process_result.ProcessResult ] ] = []
        self._page_ui.set_max_page_getter( lambda:len( self._loaded_results )+1 )
        self._page_ui.set_page_change_event(
            lambda:self.show_page( self._page_ui.get_current_page() )
        )
        for i in range(self._displayer_number):
            displayer = ResultDisplayer( self )
            self._displayers_list.append( displayer )
            displayer.pack( side="top", padx=5, pady=10, fill="x" )
    #--------------------------------------------------------
    def load_processor( self, processor ):
        from .. import analysiser
        processor:analysiser.analysiser_processor.AnalysiserProcessor = processor
        results = processor.get_results()
        self._loaded_results.clear()
        i = 0
        current_list = []
        for result in results:
            current_list.append( result )
            i += 1
            if( i >= self._displayer_number ):
                i = 0
                self._loaded_results.append( current_list )
                current_list = []
        if( i > 0 ):
            self._loaded_results.append( current_list )
        self.show_page(0)
    #----------------------------------------------------------------------------------------------------
    def show_page( self, page:int ):
        if( page >= len( self._loaded_results ) ):return
        results = self._loaded_results[page]
        for i in range( len( results ) ):
            self._displayers_list[ i ].load_result( results[i] )
#========================================================================================================
class AnalysiserViewerMenu(basic_window.BasicWindow):
    def __init__(self):
        from . import (
            analysiser_selection_combobox, result_number_bar_group,
            scroll_frame, prompt_map_chart_frame, prompt_number_chart_frame,
            hex_chart
            )
        from .. import analysiser, prompt_tag

        self._current_processor:analysiser.analysiser_processor.AnalysiserProcessor = None
        ui_padding = 8
        super().__init__()
        #self.window.resizable( width=False, height=True )
        self.window.title("Uising Discriminator")
        self.option_ui_frame = tk.Frame( self.window )
        self.option_ui_frame.pack(side="left", padx=ui_padding, pady=ui_padding)
        frame_height = 850
        # 提示詞數量分析 UI
        self.prompt_number_ui_frame = scroll_frame.ScrollFrame( self.window, text="Influence of Prompts Number", width=275, height=frame_height )
        self.prompt_number_ui_frame.pack(side="left", padx=ui_padding, pady=ui_padding)
        self.prompt_number_bar_group_table:dict[ int, result_number_bar_group.ResultNumberBarGroup ] = {}
        for i in range(1, 25):
            bar_group = result_number_bar_group.ResultNumberBarGroup(
                self.prompt_number_ui_frame.get_frame(), title="Prompts Number:{0}".format(i) )
            bar_group.get_frame().pack(side="top", padx=10, pady=4)
            self.prompt_number_bar_group_table[ i ] = bar_group
        self.prompt_number_ui_frame.update_scrollregion()
        # 提示詞影響分析 UI
        self.prompt_group_ui_frame = scroll_frame.ScrollFrame( self.window, text="Influence between Prompts", width=275, height=frame_height )
        self.prompt_group_ui_frame.pack(side="left", padx=ui_padding, pady=ui_padding)
        self.prompt_group_bar_group_table:dict[ str, result_number_bar_group.ResultNumberBarGroup ] = {}
        for i in prompt_tag.get_all_prompts():
            bar_group = result_number_bar_group.ResultNumberBarGroup(
                self.prompt_group_ui_frame.get_frame(), title="Influence from \"{0}\"".format(i) )
            bar_group.get_frame().pack(side="top", padx=10, pady=4)
            self.prompt_group_bar_group_table[i] = bar_group
        self.prompt_group_ui_frame.update_scrollregion()
        # 模型選擇群組
        self.analysiser_selection_frame = tk.LabelFrame( self.option_ui_frame, text="Discriminator Selection" )
        self.analysiser_selection_frame.grid( column=0, row=0, padx=5, pady=5 )

        self.analysiser_selecter = analysiser_selection_combobox.AnalysiserSelectionCombobox(self.analysiser_selection_frame)
        self.analysiser_selecter.selection_combobox.grid( column=0, row=0, padx=5, pady=5 )
        self.analysiser_selecter.set_on_selected_event( self._update_info_label )

        self.selected_core_info_label = tk.Label( self.analysiser_selection_frame, text="" )
        self.selected_core_info_label.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )

        self.start_process_button = tk.Button( self.analysiser_selection_frame, text="Start", command=self._click_to_start_process )
        self.start_process_button.grid( column=1, row=0, padx=5, pady=5 )
        # 篩選群組
        self.result_filter_frame = tk.LabelFrame( self.option_ui_frame, text="Data Filter" )
        self.result_filter_frame.grid( column=0, row=2, padx=5, pady=5, sticky="we" )
        self.without_training_data_var = tk.BooleanVar( self.window )
        self.without_training_data_var.set(True)
        self.without_training_data_button = tk.Checkbutton( self.result_filter_frame, text="Exclude Training Data", variable=self.without_training_data_var )
        self.without_training_data_button.grid( column=0, row=0, padx=5, pady=5 )
        self.filter_with_checkpoint_var = tk.BooleanVar(self.window)
        self.filter_with_checkpoint_var.set(True)
        self.filter_with_checkpoint_button = tk.Checkbutton( self.result_filter_frame, text="Only Target Checkpoint", variable=self.filter_with_checkpoint_var )
        self.filter_with_checkpoint_button.grid( column=0, row=1, padx=5, pady=5 )
        
        # 整體分析結果
        self.main_result_bar_group = result_number_bar_group.ResultNumberBarGroup( self.option_ui_frame, title="Overall AVG Result" )
        self.main_result_bar_group.get_frame().grid( column=0, row=3, padx=4, pady=4 )

        # 右側顯示框
        self.right_frame = scroll_frame.ScrollFrame( self.window, text = "", width=700, height=frame_height )
        self.right_frame.pack(side="left", padx=ui_padding, pady=ui_padding)
        # 個別結果顯示
        self.displayer_frame = DisplayerFrame( self.right_frame.get_frame() )
        # 提示詞數量關係表
        self.prompt_number_chart = prompt_number_chart_frame.PromptNumberChartFrame( self.right_frame.get_frame() )
        # 提示詞彼此影響
        self.prompt_map_chart = prompt_map_chart_frame.PromptMapChartFrame( self.right_frame.get_frame() )
        self.prompt_correct_hex_chart = hex_chart.HexChart( self.right_frame.get_frame() )
        self.prompt_lack_hex_chart = hex_chart.HexChart( self.right_frame.get_frame() )
        self.prompt_redundant_hex_chart = hex_chart.HexChart( self.right_frame.get_frame() )
        # 右側選項框
        self.right_option_frame = tk.LabelFrame( self.window )
        self.right_option_frame.pack(side="left", padx=ui_padding, pady=ui_padding)
        tk.Button( self.right_option_frame, text="Single Image Result", command=self._show_displayer_frame ).pack(side="top", padx=8, pady=8)
        tk.Button( self.right_option_frame, text="Number of Prompts Influence", command=self._show_prompt_number_chart ).pack(side="top", padx=8, pady=8)
        tk.Button( self.right_option_frame, text="Prompts-Prompts Influence", command=self._show_prompt_map_chart ).pack(side="top", padx=8, pady=8)
        self.window_center()
        self._update_info_label()
    #---------------------------------------------------------------------------------------------------
    def _show_displayer_frame(self):
        self.prompt_number_chart.pack_forget()
        self.displayer_frame.pack()
        self.prompt_map_chart.pack_forget()
        self.prompt_correct_hex_chart.pack_forget()
        self.prompt_lack_hex_chart.pack_forget()
        self.prompt_redundant_hex_chart.pack_forget()
        self.right_frame.update_scrollregion()
    #---------------------------------------------------------------------------------------------------
    def _show_prompt_number_chart(self):
        self.prompt_number_chart.pack()
        self.displayer_frame.pack_forget()
        self.prompt_map_chart.pack_forget()
        self.prompt_correct_hex_chart.pack_forget()
        self.prompt_lack_hex_chart.pack_forget()
        self.prompt_redundant_hex_chart.pack_forget()
        self.right_frame.update_scrollregion()
    #---------------------------------------------------------------------------------------------------
    def _show_prompt_map_chart(self):
        self.prompt_number_chart.pack_forget()
        self.displayer_frame.pack_forget()
        self.prompt_map_chart.pack()
        self.prompt_correct_hex_chart.pack()
        self.prompt_lack_hex_chart.pack()
        self.prompt_redundant_hex_chart.pack()
        self.right_frame.update_scrollregion()
    #---------------------------------------------------------------------------------------------------
    def _click_to_start_process(self)->None:
        from . import messagebox, result_number_bar_group
        from .. import analysiser, gc, prompt_tag
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
        if( self._current_processor != None ):self._current_processor.free()
        self._current_processor = analysiser.analysiser_processor.AnalysiserProcessor(
            core=core,
            without_training_data=self.without_training_data_var.get(),
            filter_with_checkpoint= self.filter_with_checkpoint_var.get(),
            )
        gc.collect()
        analysiser.torch.cuda.empty_cache()
        self._current_processor.start()
        # 更新UI
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
        # 更新多邊形圖
        self.prompt_correct_hex_chart.reset(max_value=0.75, min_value=0.25)
        self.prompt_lack_hex_chart.reset(max_value=0.5, min_value=0)
        self.prompt_redundant_hex_chart.reset(max_value=0.5, min_value=0)
        for i in prompt_tag.get_all_prompts():
            unifier = self._current_processor.get_unifier_with_prompt_group( i )
            if( unifier==None ):continue
            self.prompt_correct_hex_chart.add_data( i, unifier.get_avg_correct_rate() )
            self.prompt_lack_hex_chart.add_data( i, unifier.get_avg_lack_rate() )
            self.prompt_redundant_hex_chart.add_data( i, unifier.get_avg_redundant_rate() )
        # 處理多邊形標題
        target_prompts_tuple = self._current_processor.get_core().get_info().get_prompts()
        target_prompts = " "
        for i in target_prompts_tuple:
            target_prompts += "[{0}] ".format(i)
        self.prompt_correct_hex_chart.set_title( "Correct Rate\n{0}".format(target_prompts) )
        self.prompt_lack_hex_chart.set_title( "Lack Rate\n{0}".format(target_prompts) )
        self.prompt_redundant_hex_chart.set_title( "Redundant Rate\n{0}".format(target_prompts) )
        self.prompt_correct_hex_chart.draw_chart()
        self.prompt_lack_hex_chart.draw_chart()
        self.prompt_redundant_hex_chart.draw_chart()

        self.displayer_frame.load_processor( self._current_processor )
        self.prompt_number_chart.load_processor( self._current_processor )
        self.prompt_map_chart.load_processor( self._current_processor )
        self.right_frame.update_scrollregion()
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
            info_msg += " [{0}] ".format(p)
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
        self.right_frame.update_scrollregion()
#========================================================================================================