from . import torch
from . import basic_block
nn = torch.nn

_instance = None
#=================================================================================
class ImageAnalysiser( nn.Module ):
    def __init__(self, core):
        from . import analysiser_core
        super( ImageAnalysiser, self ).__init__()
        self.core:analysiser_core.AnalysiserCore = core
        self._have_weight = False

        self.start_layer = nn.Sequential(
            nn.Conv2d(
                in_channels=3, out_channels=8,
                kernel_size=4, padding=1, stride=2, padding_mode="reflect"
            ),
            nn.LeakyReLU( 0.2 ),
        )
        self.main = nn.Sequential(
            basic_block.ConvBlock(
                in_channels = 8,
                out_channels = 16,
                conv_mode = basic_block.ConvBlock.DOWN_SAMPLE,
                non_linear_act = basic_block.ConvBlock.LEAKY_RELU,
                have_drop_out = True
            ),
            basic_block.ConvBlock(
                in_channels = 16,
                out_channels = 32,
                conv_mode = basic_block.ConvBlock.DOWN_SAMPLE,
                non_linear_act = basic_block.ConvBlock.LEAKY_RELU,
                have_drop_out = True
            ),
        )
        self.end_layer = nn.Sequential(
                nn.Conv2d(
                    in_channels=32,
                    out_channels=64,
                    kernel_size=4, padding=1, stride=1, padding_mode="reflect", bias=False
                ),
                nn.BatchNorm2d( 64 ),
                nn.LeakyReLU(0.2),
                nn.Conv2d(
                    in_channels=64,
                    out_channels=1,
                    kernel_size=4, padding=1, stride=1, padding_mode="reflect"
                ),
                #nn.Tanh(),
            )
#---------------------------------------------------------------------------------
    def forward(self, x:torch.Tensor):
        if( len( x.size() )==2 ):x = x.unsqueeze(0)
        if( len( x.size() )==3 ):x = x.unsqueeze(0)
        x = (x + torch.rand_like(x))/2
        x = self.start_layer( x )
        x = self.main( x )
        x = self.end_layer( x )
        return x
#---------------------------------------------------------------------------------
    def have_weight(self)->bool:return self._have_weight
#---------------------------------------------------------------------------------
    def load_weight(self):
        from .. import os
        if( self.core==None ):return
        file_path = self.core.get_file_handler().get_weight_file_path()
        if( not os.path.exists( file_path ) ):
            print( "路徑:{0}\n不存在".format(file_path) )
            return
        self._have_weight = True
        self.load_state_dict( torch.load( file_path ) )
        print("成功載入權重")
#=================================================================================
def get_instance()->ImageAnalysiser:
    global _instance
    if( _instance==None ):
        _instance = ImageAnalysiser(None)
    return _instance
#----------------------------------------------------------------------------------