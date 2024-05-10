from . import tk
from . import basic_window

class WaitSDWindow(basic_window.BasicWindow):
    def __init__(self) -> None:
        from . import main_menu
        super().__init__()
        self.window.title("Waiting Stable Diffusion")
        self.window.geometry("400x50+150+150")
        tk.Label( self.window, text="等待 Stable Diffusion 開啟中..." ).place(x=50, y=10)
        self.window_center()
    #-------------------------------------------------------------------------------------
    def open(self):
        def thread_function():
            from .. import api_handler
            if( api_handler.check_sd_enable() ):
                self.close()
                return
            self.window.after(100, thread_function)
        self.window.after(100, thread_function)
        super().open()
#=========================================================================================