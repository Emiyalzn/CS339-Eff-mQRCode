#!/bin/bash
epoch_array=(20 40 60 80 100 120 160 200)
subsets=('best' 'dist' 'angle')
for epoch in ${epoch_array[@]}
do
  for subset in ${subsets[@]}
  do
    CUDA_VISIBLE_DEVICES=0 python test.py --dataroot ./datasets/qrcode --subset ${subset} --epoch ${epoch} --name deblurPix2PixGAN --model deblurQr_pix2pix_gan  --batch_size 1 --resize_or_crop scale_width_and_crop --no_flip
  done
done