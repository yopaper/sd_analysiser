from . import tk
from . import basic_window

_instance = None

class MainMenu(basic_window.BasicWindow):
    #-------------------------------------------------------------------------------------
    def __init__(self):
        from . import prompt_manager_menu, checkpoint_set_menu, image_generator_menu, image_viewer_menu, analysiser_option_menu, analysiser_viewer_menu
        def open_manager_menu():
            #self.close()
            prompt_manager_menu.PromptManagerMenu().open()
        #.................................................................................
        def open_checkpoint_menu():
            #self.close()
            checkpoint_set_menu.CheckPointSetMenu().open()
        #.................................................................................
        def open_image_generator_menu():
            #self.close()
            image_generator_menu.ImageGeneratorMenu().open()
        #.................................................................................
        def open_image_viewer_menu():
            #self.close()
            image_viewer_menu.ImageViewerMenu().open()
        #.................................................................................
        self.window = tk.Tk()
        self.window.title("Main Menu")
        self.window.resizable(False, False)

        self.prompt_manager_button = tk.Button(
            self.window, text="Prompts Management", command=open_manager_menu )
        self.prompt_manager_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.image_data_frame = tk.LabelFrame(
            self.window, text="Images"
        )
        self.image_data_frame.grid( row=0, column=1, padx=5, pady=5 )

        self.image_viewer_button = tk.Button(
            self.image_data_frame, text="Image Data Viewer", command=open_image_viewer_menu )
        self.image_viewer_button.grid( row=0, column=0, padx=5, pady=5 )

        self.image_generator_menu_button = tk.Button(
            self.image_data_frame, text="Image Generator", command=open_image_generator_menu )
        self.image_generator_menu_button.grid( row=1, column=0, padx=5, pady=5 )

        self.analysiser_frame = tk.LabelFrame(
            self.window, text="Discriminator"
        )
        self.analysiser_frame.grid( row=0, column=2, padx=5, pady=5 )
    
        self.analysiser_option_button = tk.Button(
            self.analysiser_frame, text="Discriminator Management", command=lambda: analysiser_option_menu.AnalysiserOptionMenu().open() )
        self.analysiser_option_button.grid( row=0, column=0, padx=5, pady=5 )

        self.analysiser_viewer_button = tk.Button(
            self.analysiser_frame, text="Discriminator Using", command=lambda: analysiser_viewer_menu.AnalysiserViewerMenu().open() )
        self.analysiser_viewer_button.grid( row=1, column=0, padx=5, pady=5 )

        self.checkpoint_menu_button = tk.Button(
            self.window, text="Checkpoint", command=open_checkpoint_menu )
        self.checkpoint_menu_button.grid(row=0, column=5, padx=5, pady=5)

        self.button_ui = (
            self.prompt_manager_button, self.checkpoint_menu_button,
            self.image_generator_menu_button, self.image_viewer_button,
            self.analysiser_option_button, self.analysiser_viewer_button )

        self.window_center()
    #-------------------------------------------------------------------------------------
    def disable_buttons(self):
        for button in self.button_ui:
            button.config(state="disabled")
    #-------------------------------------------------------------------------------------
    def enable_buttons(self):
        for button in self.button_ui:
            button.config(state="normal")
    #-------------------------------------------------------------------------------------
    def open(self):
        self.window.mainloop()
    #-------------------------------------------------------------------------------------
    def close(self):
        self.window.destroy()
#=========================================================================================

def get_instance()->MainMenu:
    global _instance
    if( _instance==None ):
        _instance = MainMenu()
    return _instance
#-----------------------------------------------------------------------------------------