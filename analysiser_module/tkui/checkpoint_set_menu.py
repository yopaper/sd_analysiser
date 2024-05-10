from . import tk
from . import basic_window

class CheckPointSetMenu(basic_window.BasicWindow):
    def __init__(self):
        from .. import checkpoints_loader
        super().__init__()
        self.window.title("設定Checkpoint")
        # Checkpoin 按鈕群組
        tk.Label(self.window, text="可用的Checkpoint").grid(row=0, column=0)
        self.selected_checkpoint_title = tk.StringVar()
        self.checkpoint_button_table = {}
        i = 1
        for cp in checkpoints_loader.checkpoint_list:
            cp_button = tk.Radiobutton( self.window, text=cp.name, variable=self.selected_checkpoint_title, value=cp.title )
            cp_button.grid( column=0, row=i )
            self.checkpoint_button_table[ cp.title ] = cp_button
            i += 1
        self.checkpoint_button_table[ checkpoints_loader.current_checkpoint.title ].select()
        # 其他按鈕
        self.exit_button = tk.Button( self.window, text="關閉", command=self.close )
        self.exit_button.grid(row=0, column=1)
        self.apply_button = tk.Button( self.window, text="套用" )
        self.window_center()
#=========================================================================================