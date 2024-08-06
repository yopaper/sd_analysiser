
class PageUI:
    def __init__(self, master) -> None:
        from . import tk
        self._current_page = 0
        self._max_page_getter = None
        self._after_page_change = None
        self.main_frame = tk.LabelFrame( master=master, text="Page" )
        self.last_page_button = tk.Button( self.main_frame, text="Next", command=lambda delta=-1:self._change_page( delta=delta ) )
        self.last_page_button.grid( column=0, row=0, padx=8, pady=8 )
        self.next_page_button = tk.Button( self.main_frame, text="Last", command=lambda delta= 1:self._change_page( delta=delta ) )
        self.next_page_button.grid( column=2, row=0, padx=8, pady=8 )
        self.page_label = tk.Label( self.main_frame, text="" )
        self.page_label.grid( column=1, row=0, padx=8, pady=8 )
    #--------------------------------------------------------------------
    def get_current_page(self)->int:return self._current_page
    #--------------------------------------------------------------------
    def get_max_page(self)->int:
        if( self._max_page_getter != None ):
            return self._max_page_getter()
        return None
    #--------------------------------------------------------------------
    def set_max_page_getter(self, getter):
        self._max_page_getter = getter
    #--------------------------------------------------------------------
    def set_page_change_event(self, event):
        self._after_page_change = event
    #--------------------------------------------------------------------
    def update_state(self):
        self._change_page( 0 )
    #--------------------------------------------------------------------
    def _change_page(self, delta:int=0):
        self._current_page += delta
        max_page = self.get_max_page()
        if( self._current_page < 0 ):
            if( max == None ):self._current_page = 0
            else:self._current_page = max_page-1
        elif( max_page!=None and self._current_page >= max_page ):
            self._current_page = 0
        self._on_page_change()
    #--------------------------------------------------------------------
    def _on_page_change(self):
        if( self._max_page_getter!=None ):
            max_page:int = self._max_page_getter()
            self.page_label.config( text="{0}/{1}".format( self._current_page+1, max_page+1 ) )
        else:
            self.page_label.config( text=str(self._current_page+1) )
        if( self._after_page_change!=None ):
            self._after_page_change()
#========================================================================