from . import torch
from . import basic_block
nn = torch.nn
class ImageAnalysiser( torch.Module ):
    def __init__(self, name:str):
        super( ImageAnalysiser, self ).__init__()
        self.name = name
        
        self.start_layer = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels, out_channels=dim_counter.get(0),
                kernel_size=4, padding=1, stride=2, padding_mode="reflect"
            ),
            nn.LeakyReLU( 0.2 ),
        )
        self.main = nn.Sequential(
            basic_block.ConvBlock(
                in_channels = dim_counter.get(0),
                out_channels = dim_counter.get(1),
                conv_mode = basic_block.ConvBlock.DOWN_SAMPLE,
                non_linear_act = basic_block.ConvBlock.LEAKY_RELU,
                have_drop_out = False
            ),
            basic_block.ConvBlock(
                in_channels = dim_counter.get(1),
                out_channels = dim_counter.get(2),
                conv_mode = basic_block.ConvBlock.DOWN_SAMPLE,
                non_linear_act = basic_block.ConvBlock.LEAKY_RELU,
                have_drop_out = False
            ),
        )
        self.end_layer = nn.Sequential(
                nn.Conv2d(
                    in_channels=dim_counter.get(2),
                    out_channels=dim_counter.get(3),
                    kernel_size=4, padding=1, stride=1, padding_mode="reflect", bias=False
                ),
                nn.BatchNorm2d( dim_counter.get(3) ),
                nn.LeakyReLU(0.2),
                nn.Conv2d(
                    in_channels=dim_counter.get(3),
                    out_channels=1,
                    kernel_size=4, padding=1, stride=1, padding_mode="reflect"
                ),
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
#=================================================================================