from . import torch
from torch.utils.data import Dataset

class DataSpliter:
    from .. import image_data_filter
    def __init__(self, data_filter:image_data_filter.ImageDataFilter) -> None:
        self._train_positive_data = []
        self._train_negative_data = []
        self._test_positive_data = []
        self._test_negative_data = []
#======================================================================================
class AnalysiserDataset(Dataset):
    from .. import image_data_filter
    def __init__(self, data_filter:image_data_filter):
        self._image_data_list = []
        self._label_list = []
