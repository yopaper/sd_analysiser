from . import basic_window
from . import tk, ttk

class AnalysiserOptionMenu(basic_window.BasicWindow):
    from .. import analysiser
    def __init__(self):
        from . import filter_ui, analysiser_selection_combobox
        from .. import prompt_tag, analysiser
        super().__init__()
        self.window.title("Discriminator")

        self.analysiser_manager_frame = tk.LabelFrame( self.window, text="Management" )
        self.analysiser_manager_frame.grid( column=0, row=0, padx=6, pady=6 )
        tk.Label( self.analysiser_manager_frame, text="Discriminator Selection" ).grid(column=0, row=0, padx=5, pady=5)
        self.analysiser_selecter = analysiser_selection_combobox.AnalysiserSelectionCombobox( self.analysiser_manager_frame )
        self.analysiser_selecter.selection_combobox.grid( column=1, row=0, padx=5, pady=5 )
        self.analysiser_selecter.set_on_selected_event( self._update_ui )

        # 管理按鈕列
        self.button_row_frame = tk.Frame( self.analysiser_manager_frame )
        self.button_row_frame.grid( column=0, row=1, columnspan=2, padx=5, pady=5 )
        self.create_analysiser_button = tk.Button( self.button_row_frame, text="Create", command=self._click_to_create_analysiser )
        self.create_analysiser_button.grid( column=0, row=0, padx=5, pady=5 )
        #self.rename_analysiser_button = tk.Button( self.button_row_frame, text="Rename" )
        #self.rename_analysiser_button.grid( column=1, row=0, padx=5, pady=5 )
        self.delete_analysiser_button = tk.Button( self.button_row_frame, text="Delete" )
        self.delete_analysiser_button.grid( column=2, row=0, padx=5, pady=5 )

        # 資料篩選 UI
        self.train_data_filter_frame = tk.LabelFrame(self.window, text="Training Data Filter")
        self.train_data_filter_frame.grid( column=1, row=0, rowspan=3, padx=6, pady=6 )

        self.data_number_label = tk.Label(self.train_data_filter_frame)
        self.data_number_label.grid( column=0, row=0 )
        self.data_filter_ui = filter_ui.FullFilterUI( self.train_data_filter_frame )
        self.data_filter_ui.grid( column=0, row=1 )
        self.data_filter_ui.set_click_event( self._update_data_number_ui )

        # 訓練參數........................................................................................
        self.train_parameters_frame = tk.LabelFrame( self.window, text="Training Parameters" )
        self.train_parameters_frame.grid( column=0, row=1, padx=6, pady=6 )
        # Epoch
        tk.Label( self.train_parameters_frame, text="Epoch" ).grid( column=0, row=0, padx=6, pady=6 )
        self.train_epoch_spinbox = tk.Spinbox( self.train_parameters_frame, from_=1, to=890604 )
        self.train_epoch_spinbox.grid( column=1, row=0, padx=6, pady=6 )
        # Learning Rate
        tk.Label( self.train_parameters_frame, text="Learning Rate" ).grid( column=0, row=1, padx=6, pady=6 )
        self.learning_rate_var = tk.StringVar( self.window )
        self.learning_rate_var.set( "2e-4" )
        self.learning_rate_entry = tk.Entry( self.train_parameters_frame, textvariable=self.learning_rate_var )
        self.learning_rate_entry.grid( column=1, row=1, padx=6, pady=6 )
        # Batch Size
        tk.Label( self.train_parameters_frame, text="Batch Size" ).grid( column=0, row=2, padx=6, pady=6 )
        self.batch_size_var = tk.StringVar( self.window )
        self.batch_size_var.set( "16" )
        self.batch_size_entry = tk.Entry( self.train_parameters_frame, textvariable=self.batch_size_var )
        self.batch_size_entry.grid( column=1, row=2, padx=6, pady=6 )

        self.start_train_button = tk.Button( self.train_data_filter_frame, text="Start Training", command=self.start_train )
        self.start_train_button.grid( column=0, row=2 )

        # 模型資訊
        self.info_ui_frame = tk.LabelFrame( self.window, text="Discriminator Information" )
        self.info_ui_frame.grid( row=2, column=0, padx=6, pady=6 )
        self.info_label = tk.Label(self.info_ui_frame, text="", justify="left")
        self.info_label.grid( row=0, column=0, padx=6, pady=6 )

        self.data_filter_ui.update()
        self._update_ui()
        self.window_center()
    #---------------------------------------------------------------------------
    def get_selected_core(self)->analysiser.analysiser_core.AnalysiserCore:
        return self.analysiser_selecter.get_selected_core()
    #---------------------------------------------------------------------------
    def start_train(self)->None:
        from .. import analysiser, messagebox
        core = self.get_selected_core()
        if( core==None ):
            messagebox.showerror("Training Error", "Not select Discriminator yet!")
            return
        epoch:int = 0
        try:
            epoch += int(self.train_epoch_spinbox.get())
        except:
            messagebox.showerror("Training Error", "Epoch Error!")
            return
        learning_rate:float = 0
        try:
            learning_rate += float( self.learning_rate_var.get() )
        except:
            messagebox.showerror("Training Error", "Learning Rate Error!")
            return
        batch_size:int = 0
        try:
            batch_size += int( self.batch_size_var.get() )
        except:
            messagebox.showerror("Training Error", "Batch Size Error!")
            return

        data_filter = self.data_filter_ui.current_filter
        print( "建立訓練器" )
        trainer = analysiser.analysiser_trainer.AnalysiserTrainer(
            analysiser_core = core,
            data_filter=data_filter,
            epoch = epoch,
            learn_rate = learning_rate,
            batch_size = batch_size,
        )
        trainer.start_train()
        core.info.load_info()
        self._update_ui()
        analysiser.analysiser_core.write_to_file()
    #---------------------------------------------------------------------------
    def _update_ui(self, event=None)->None:
        core = self.get_selected_core()
        if( core==None ):
            self.info_label.config(text="Not select Discriminator")
            return
        info = core.get_info()
        info.load_info()
        if( len( info.get_info_dict() )==0 ):
            self.info_label.config(text="No Discriminator information!\nInformation will be created after training.")
            return
        
        info_msg = "\n"
        info_msg += "Discriminator Name: {0}\n".format(core.get_name() )
        info_msg += "Target Prompt: {0}\n".format(info.get_prompts())
        checkpoint = info.get_checkpoint()
        if( checkpoint!=None ):
            info_msg += "Checkpoint: [{0}]\n".format( checkpoint.name )
        else:info_msg += "Checkpoint: None\n"
        info_msg += "Training Epoch: {0}\n".format(info.get_epoch())
        info_msg += "Training Batch Size: {0}\n".format( info.get_batch_size() )
        info_msg += "Training Learning Rate: {0}\n".format( info.get_learning_rate() )
        info_msg += "Training Data Number: {0}\n".format( len( info.get_training_data_name_list() ) )
        info_msg += "Lowest Training Loss: {0}\n".format( round( float( info.get_min_train_loss() ) * 1e3) / 1e3 )
        self.info_label.config( text=info_msg )
    #---------------------------------------------------------------------------
    def _update_data_number_ui(self):
        from .. import analysiser
        data_filter = self.data_filter_ui.current_filter
        data_spliter = analysiser.analysiser_dataset.DataSpliter( data_filter )
        train_pos, train_neg = data_spliter.get_train_data()
        test_pos, test_neg = data_spliter.get_test_data()
        label_msg = "Positive Training:{0}\nPositive Test:{1}\nNegative Training:{2}\nnNegative Test:{3}".format(
            len( train_pos ), len( test_pos ),
            len( train_neg ), len( test_neg ),
        )
        self.data_number_label.config( text=label_msg )
    #---------------------------------------------------------------------------
    def _click_to_create_analysiser(self):
        from .. import simpledialog, analysiser
        intput_name = simpledialog.askstring(title="Create New Discriminator", prompt="Input the Name for New Discriminator")
        if( intput_name==None ):return
        analysiser.analysiser_core.create_core( intput_name )
        self.analysiser_selecter.update_selection()
#===============================================================================