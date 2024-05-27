
class AnalysiserSelectionCombobox:
    from .. import analysiser
    def __init__(self, master):
        from . import ttk, tk
        from .. import analysiser
        self.selection_combobox = ttk.Combobox(master=master, state="readonly")
        self.update_selection()
    #---------------------------------------------------------------------------------------------------
    def get_selected_core(self)->analysiser.analysiser_core.AnalysiserCore:
        from .. import analysiser
        return analysiser.analysiser_core.get_core_with_name( self.selection_combobox.get() )
    #---------------------------------------------------------------------------------------------------
    def update_selection(self)->None:
        from .. import analysiser
        self.selection_combobox.config( values=[i.get_name() for i in analysiser.analysiser_core.get_all_alalysisers()] )
    #---------------------------------------------------------------------------------------------------
    def set_on_selected_event(self, event):
        self.selection_combobox.bind( "<<ComboboxSelected>>", event )
#=======================================================================================================