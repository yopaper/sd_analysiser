from . import tk

class BasicWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.protocol( "WM_DELETE_WINDOW", self.close )
    #---------------------------------------------------------
    def open(self):
        from . import main_menu
        main_menu.get_instance().disable_buttons()
        self.window.mainloop()
    #---------------------------------------------------------
    def close(self):
        from . import main_menu
        main_menu.get_instance().enable_buttons()
        self.window.destroy()
    #---------------------------------------------------------
    def window_center(self, delay_time:int=10):
        def delay_function():
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            pos_x = int( screen_width/2 ) - int(window_width/2)
            pos_y = int( screen_height/2 ) - int(window_height/2)
            self.window.geometry("+{0}+{1}".format(pos_x, pos_y))
        self.window.after( delay_time, delay_function )
#=========================================================================