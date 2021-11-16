#!/bin/bash
epoch_array=(20 40 60 80 100 120 160 200)
for epoch in ${epoch_array[@]}
do
  CUDA_VISIBLE_DEVICES=0 python test.py --dataroot ./datasets/qrcode --epoch ${epoch} --name deblurPix2PixGAN_default --model deblurQr_pix2pix_gan  --batch_size 1 --resize_or_crop scale_width_and_crop --no_flip
done