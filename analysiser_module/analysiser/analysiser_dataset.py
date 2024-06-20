from . import torch, torch_data

class DataSpliter:
    #from .. import image_data_handler
    def __init__(self, data_filter,
                 max_train_data_number:int=1024,
                 max_test_data_number:int=256):
        from random import randint
        from .. import image_data_filter
        self._train_positive_data = []
        self._train_negative_data = []
        self._test_positive_data = []
        self._test_negative_data = []
        data_filter:image_data_filter.ImageDataFilter = data_filter
        positive_data = data_filter.get_result()
        for data in positive_data:
            if( data.for_test() ):
                self._test_positive_data.append( data )
            else:self._train_positive_data.append( data )
        negative_data = data_filter.get_negative_result()
        for data in negative_data:
            if( data.for_test() ):
                self._test_negative_data.append( data )
            else:self._train_negative_data.append(data)
        # 篩選直到符合資料數上限
        def limit_data_list( positive_list:list, negative_list:list, max_number:int ):
            if( max_number==None ):return
            while( len( positive_list ) + len( negative_list ) > max_number ):
                if( len( negative_list ) >= len( positive_list ) ):
                    index = randint( 0, len( negative_list )-1 )
                    del negative_list[index]
                else:
                    index = randint( 0, len( positive_list )-1 )
                    del positive_list[index]
        #...............................................................................
        def limit_train_data_number():
            limit_data_list(
                positive_list=self._train_positive_data,
                negative_list=self._train_negative_data,
                max_number=max_train_data_number
            )
        #...............................................................................
        def limit_test_data_number():
            limit_data_list(
                positive_list=self._test_positive_data,
                negative_list=self._test_negative_data,
                max_number=max_test_data_number
            )
        #..............................................................................
        limit_train_data_number()
        limit_test_data_number()
    #----------------------------------------------------------------------------------
    def get_train_data(self):
        from .. import image_data_handler
        pos_data:tuple[ image_data_handler.ImageData ] = self._train_positive_data
        neg_data:tuple[ image_data_handler.ImageData ] = self._train_negative_data
        return pos_data, neg_data
    #----------------------------------------------------------------------------------
    def get_test_data(self):
        from .. import image_data_handler
        pos_data:tuple[ image_data_handler.ImageData ] = self._test_positive_data
        neg_data:tuple[ image_data_handler.ImageData ] = self._test_negative_data
        return pos_data, neg_data
#======================================================================================

class AnalysiserDataset(torch_data.Dataset):
    from . import torchvision, torch

    def __init__(self, positive_datas, negative_datas):
        from . import torch, torchvision, analysiser_model
        from .. import image_data_handler
        positive_datas:tuple[image_data_handler.ImageData] = positive_datas
        negative_datas:tuple[image_data_handler.ImageData] = negative_datas
        self._image_tensor_data_list = []
        self._relative_image_data_list = []
        self._label_list = []
        transformer = torchvision.transforms.ToTensor()
        model = analysiser_model.get_instance()
        for data in positive_datas:
            self._relative_image_data_list.append( data )
            image = data.get_tensor_data()
            self._image_tensor_data_list.append( image )
            self._label_list.append( torch.Tensor( [0.95] ).cuda() )
            #label = torch.ones_like( model(image) ) * 0.7
            #self._label_list.append( label.squeeze(0) )
        for data in negative_datas:
            self._relative_image_data_list.append( data )
            image = data.get_tensor_data()
            self._image_tensor_data_list.append( image )
            self._label_list.append( torch.Tensor( [0.05] ).cuda() )
            #label = torch.ones_like( model(image) ) * 0.3
            #self._label_list.append( label.squeeze(0) )
    #-----------------------------------------------------------------------------------
    def __getitem__(self, index) -> tuple[ torch.Tensor, torch.Tensor ]:
        return self._image_tensor_data_list[index], self._label_list[index]
    #-----------------------------------------------------------------------------------
    def __len__(self)->int: return len( self._image_tensor_data_list )
    #-----------------------------------------------------------------------------------
    def get_relative_image_data(self):
        from .. import image_data_handler
        image_tuple:tuple[image_data_handler.ImageData] = tuple( self._relative_image_data_list )
        return image_tuple
#=======================================================================================