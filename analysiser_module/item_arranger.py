
class ItemArranger:
    def __init__(self, items, pick_number:int):
        assert pick_number <= len( items ), "pick_number 必須小於等於 items 的長度"
        assert pick_number >= 0, "pick_number 必須大於等於 0"
        self.items = tuple( items )
        self.pick_index = [i for i in range(pick_number)]
        self.end = False
        if( pick_number == 0 ):
            self.end = True
    #----------------------------------------------------------------------------
    def get_index(self):
        return tuple( self.pick_index )
    #----------------------------------------------------------------------------
    def get_item(self)->tuple:
        return tuple([self.items[i] for i in self.pick_index])
    #----------------------------------------------------------------------------
    def is_end(self):
        return self.end
    #----------------------------------------------------------------------------
    def next(self):
        if( self.end ):return
        item_len = len( self.items )
        index_len = len( self.pick_index )
        #........................................................................
        def process_index(index):
            if( index<0 ):
                self.end = True
                return
            head_index = self.pick_index[ index ]
            for i in range( index, index_len ):
                head_index += 1
                if( head_index >= item_len ):
                    process_index( index-1 )
                    return
                self.pick_index[ i ] = head_index
        #........................................................................
        process_index( index_len-1 )
#================================================================================