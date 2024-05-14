from . import basic_module
from . import basic_block
from . import model_dim_counter
from .. import torch; nn = torch.nn

class Discriminator( basic_module.WeightModule ):
    def __init__(self, name:str, in_channels:int, dim_counter:model_dim_counter.DimCounter):
        super( Discriminator, self ).__init__( name )
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

class DiscriminatorOld( basic_module.WeightModule ):
    def __init__(self, name:str, input_dim:int, dim_counter:model_dim_counter.DimCounter, drop_rate:float=0.5):
        super(DiscriminatorOld, self).__init__(name)
        self.main = nn.Sequential(
            basic_module.NormalConv(
                in_dim=input_dim, 
                out_dim=dim_counter.get(0),
                kernel_size=5,
                stride=1,
                conv_bias=False
            ),
            basic_module.NormalConv(
                in_dim=dim_counter.get(0),
                out_dim=dim_counter.get(1),
                kernel_size=5,
                stride=2,
                conv_bias=False
            ),
            nn.Dropout2d( drop_rate ),
            basic_module.NormalConv(
                in_dim=dim_counter.get(1),
                out_dim=dim_counter.get(2),
                kernel_size=5,
                stride=1,
                conv_bias=False
            ),
            basic_module.NormalConv(
                in_dim=dim_counter.get(2),
                out_dim=dim_counter.get(3),
                kernel_size=5,
                stride=2,
                conv_bias=False
            ),
            nn.Dropout2d( drop_rate ),
            basic_module.NormalConv(
                in_dim=dim_counter.get(3),
                out_dim=dim_counter.get(4),
                kernel_size=5,
                stride=1,
                conv_bias=False
            ),
            basic_module.NormalConv(
                in_dim=dim_counter.get(4),
                out_dim=dim_counter.get(5),
                kernel_size=5,
                stride=2,
                conv_bias=False
            ),
            nn.Dropout2d( drop_rate ),
            nn.AdaptiveAvgPool3d( ( dim_counter.get(5), 1, 1 ) ),
            nn.Flatten( 1, 3 ),
            basic_module.BasicLinearLayer( dim_counter.get(5), dim_counter.get(3) ),
            basic_module.BasicLinearLayer( dim_counter.get(3), 1 ),
            nn.Sigmoid()
        )
    #------------------------------------------------------------------------------
    def forward(self, input):
        if( len( input.size() )==2 ):input = input.unsqueeze(0)
        if( len( input.size() )==3 ):input = input.unsqueeze(1)
        return self.main(input)
#=================================================================================