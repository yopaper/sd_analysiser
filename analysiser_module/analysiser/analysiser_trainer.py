
class AnalysiserTrainer:
    from . import analysiser_dataset, analysiser_core
    from .. import image_data_filter
    def __init__(self,
        analysiser_core: analysiser_core.AnalysiserCore,
        data_filter:image_data_filter.ImageDataFilter,
        epoch:int, learn_rate:float, batch_size:int
    ) -> None:
        from . import torch, torch_data, analysiser_dataset
        self.core = analysiser_core
        self.data_filter = data_filter
        data_spliter = analysiser_dataset.DataSpliter( self.data_filter )
        self.train_dataset = analysiser_dataset.AnalysiserDataset( *data_spliter.get_train_data() )
        self.test_dataset = analysiser_dataset.AnalysiserDataset( *data_spliter.get_test_data() )
        self.epoch = epoch
        self.batch_size = batch_size
        self.learn_rate = learn_rate
        self.model = self.core.get_model()
        self.loss = torch.nn.BCELoss()
        self.train_dataloader = torch_data.DataLoader(
            dataset=self.train_dataset, batch_size=self.batch_size, shuffle=True )
        self.test_dataloader = torch_data.DataLoader(
            dataset=self.test_dataset, batch_size=self.batch_size, shuffle=True )
        self.optm = torch.optim.Adam( self.model.parameters(), lr = self.learn_rate )
        self._loss_sum = 0; self._batch_count = 0
        self._min_test_loss = -1; self._min_train_loss = -1
    #---------------------------------------------------------------------------
    def get_core(self)->analysiser_core.AnalysiserCore:
        return self.core
    #---------------------------------------------------------------------------
    def get_info(self)->dict:
        from .. import info_key
        info = {}
        info[ info_key.PROMPT_KEY ] = [ p.tag() for p in self.data_filter.tags ]
        info[ info_key.EPOCH_KEY ] = self.epoch
        info[ info_key.LEARNING_RATE_KEY ] = self.learn_rate
        info[ info_key.BATCH_SIZE_KEY ] = self.batch_size
        info[ info_key.MIN_TRAIN_LOSS_KEY ] = self._min_train_loss
        info[ info_key.MIN_TEST_LOSS_KEY ] = self._min_test_loss
        return info
    #---------------------------------------------------------------------------
    def start_train(self)->None:
        from . import torch, analysiser_model
        def train_batch( data:torch.Tensor, label:bool ):
            output = self.model( data )
            #gt = torch.ones_like( output ) * label
            loss = self.loss( output, label )
            self.optm.zero_grad()
            loss.backward()
            self.optm.step()
            self._loss_sum += float( loss )
            self._batch_count += 1
        #.......................................................................
        def train_epoch():
            self._batch_count = 0
            self._loss_sum = 0
            self.model.train()
            for data, label in self.train_dataloader:
                train_batch( data, label )
            train_loss = self._loss_sum / self._batch_count
            if( self._min_train_loss<0 or train_loss<self._min_train_loss ):
                self._min_train_loss = train_loss
            print( "Train Loss:", train_loss )
        #.......................................................................
        def test_batch( data:torch.Tensor, label:bool ):
            output = self.model( data )
            #gt = torch.ones_like( output ) * label
            loss = self.loss( output, label )
            self._loss_sum += float( loss )
            self._batch_count += 1
        #.......................................................................
        def test_epoch():
            self._batch_count = 0
            self._loss_sum = 0
            self.model.eval()
            for data, label in self.train_dataloader:
                test_batch( data, label )
            test_loss = self._loss_sum / self._batch_count
            print( "Test Loss:", test_loss )
            if( self._min_test_loss < 0 or test_loss < self._min_test_loss ):
                self._min_test_loss = test_loss
                save_weight()
        #.......................................................................
        def save_info():
            from .. import json
            json_info = json.dumps( self.get_info() )
            file_path = self.core.file_handler.get_info_file_path()
            with open( file=file_path, mode="w" )as file_writer:
                file_writer.write(json_info)
        #.......................................................................
        def save_weight():
            from . import torch
            file_path = self.core.get_file_handler().get_weight_file_path()
            torch.save( self.model.state_dict(), file_path,  )
        #.......................................................................
        print("開始訓練")
        for i in range( self.epoch ):
            print("Epoch:", i+1)
            train_epoch()
            test_epoch()
        save_info()
        print("訓練完成")
#===============================================================================