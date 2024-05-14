from . import torch, nn


class ConvBlock( nn.Module ):
    DOWN_SAMPLE = 1; UP_SAMPLE = 2
    RELU = 11; LEAKY_RELU = 12
    #------------------------------------------------------------------------------------------------
    def __init__(self, in_channels:int, out_channels:int,
                 conv_mode:int, non_linear_act:int, have_drop_out:bool=True) -> None:
        super(ConvBlock, self).__init__()
        # Conv Layer
        if conv_mode==ConvBlock.DOWN_SAMPLE:
            self.conv = nn.Conv2d( in_channels=in_channels, out_channels=out_channels,
                              kernel_size=4, stride=2, padding=1, padding_mode="reflect", bias=False )
        elif conv_mode==ConvBlock.UP_SAMPLE:
            self.conv = nn.ConvTranspose2d( in_channels=in_channels, out_channels=out_channels,
                                kernel_size=4, stride=2, padding=1, bias=False )
        else:raise Exception( "The conv_mode must be ConvBlock.DOWN_SAMPLE or ConvBlock.UP_SAMPLE" )
        # Normal Layer
        self.normal_layer = nn.InstanceNorm2d( num_features=out_channels )
        # Non Linear Layer
        if non_linear_act == ConvBlock.RELU:
            self.act_layer = nn.ReLU()
        elif non_linear_act == ConvBlock.LEAKY_RELU:
            self.act_layer = nn.LeakyReLU( 0.2 )
        else:raise Exception("non_linear_act must be ConvBlock.RELU or ConvBlock.LEAKY_RELU")
        # Drop Out Layer
        self.have_drop_out = have_drop_out
        self.drop_out_layer = nn.Dropout( 0.5 )
    #-----------------------------------------------------------------------------------------------
    def forward(self, x):
        x = self.conv( x )
        x = self.normal_layer( x )
        x = self.act_layer( x )
        if( self.have_drop_out ):
            x = self.drop_out_layer( x )
        return x
#====================================================================================================