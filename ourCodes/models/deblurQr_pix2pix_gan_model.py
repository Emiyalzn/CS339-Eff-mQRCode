import torch
from util.image_pool import ImagePool
from .base_model import BaseModel
from . import networks

class DeblurQrPix2PixGANModel(BaseModel):
    def name(self):
        return 'DeblurQrCycleGANModel'

    @staticmethod
    def modify_commandline_options(parser, is_train=True):
        parser.set_defaults(pool_size=0, no_lsgan=True, norm='batch')
        parser.set_defaults(dataset_mode='aligned')
        parser.set_defaults(netG='unet_256')
        if is_train:
            parser.add_argument('--lambda_L1', type=float, default=100.0, help='weight for L1 loss')

        return parser