from . import torch, torch_data

class DataSpliter:
    from .. import image_data_filter, image_data_handler
    def __init__(self, data_filter:image_data_filter.ImageDataFilter) -> None:
        self._train_positive_data = []
        self._train_negative_data = []
        self._test_positive_data = []
        self._test_negative_data = []
        positive_data = data_filter.get_result()
        for data in positive_data:
            if( data.get_seed()%3==0 ):
                self._test_positive_data.append( data )
            else:self._train_positive_data.append( data )
        negative_data = data_filter.get_negative_result()
        for data in negative_data:
            if( data.get_seed()%3==0 ):
                self._test_negative_data.append( data )
            else:self._train_negative_data.append(data)
    #----------------------------------------------------------------------------------
    def get_train_data(self)->tuple[ tuple[image_data_handler.ImageData], tuple[image_data_handler.ImageData] ]:
        return self._train_positive_data, self._train_negative_data
    #----------------------------------------------------------------------------------
    def get_test_data(self)->tuple[ tuple[image_data_handler.ImageData], tuple[image_data_handler.ImageData] ]:
        return self._test_positive_data, self._test_negative_data
#======================================================================================
class AnalysiserDataset(torch_data.Dataset):
    from . import torchvision, torch
    from .. import image_data_filter, image_data_handler

    def __init__(self, positive_datas:tuple[image_data_handler.ImageData], negative_datas:tuple[image_data_handler.ImageData]):
        from . import torch, torchvision, analysiser_model
        self._image_data_list = []
        self._label_list = []
        transformer = torchvision.transforms.ToTensor()
        model = analysiser_model.get_instance()
        for data in positive_datas:
            image = transformer( data.get_pil_image() )
            self._image_data_list.append( image )
            label = torch.ones_like( model(image) ) * 0.95
            self._label_list.append( label.squeeze(0) )
        for data in negative_datas:
            image = transformer( data.get_pil_image() )
            self._image_data_list.append( image )
            label = torch.ones_like( model(image) ) * 0.05
            self._label_list.append( label.squeeze(0) )
    #-----------------------------------------------------------------------------------
    def __getitem__(self, index) -> tuple[ torch.Tensor, bool ]:
        return self._image_data_list[index], self._label_list[index]
    #-----------------------------------------------------------------------------------
    def __len__(self)->int:
        return len( self._image_data_list )
#=======================================================================================