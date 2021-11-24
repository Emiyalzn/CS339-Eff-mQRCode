# CS339-Project
Course Project for CS339: Computer Networks🤗.

## Things to be done:
### Code Part
- 加密算法实现（是一切的基础，毕竟得先产生数据集）-`lzn`
- 解密算法复现：`多帧拼接解码`、快速解码，先做前者-`xx,wyt`
- 数据集收集：动态生成二维码ground truth脚本（考虑2s变化一次），支架拍摄，
每个ground truth假设有30个有效帧，可以先试着收集1000个ground truth训一轮。
先做最精确距离上的训练，改变角度、改变距离的训练可以之后再说。-`xx,wyt`
- 图片处理：视频切帧，图片裁剪只留下二维码，二维码矫正成正方形，去掉模糊的二维码。-`xx,wyt`
- GAN pipeline搭建：`Cycle GAN`, WGAN，这两种可能效果比较好，有类似代码。-`lzn`
- benchmark脚本： 三种解码算法比较性能的脚本
- 部署到移动端：选做，如果时间有多可以做一个可移动的app
- 一个小idea：加密的过程也许也可以用GAN来替代，可以在做完之后试试看
### Report part
- 答辩PPT，讲稿
- 大作业报告

## Environment
- anaconda, python=3.8 (conda create -n xx python=3.8)
- opencv-python (pip install opencv-python)
- conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge -c nvidia
- pip install pillow
- pip install dominate
- pip install visdom
- connect to visdom: ssh -L 8097:127.0.0.1:8097 -p 225 lizenan@202.121.181.105
- ffmpeg

## Run Experiments

- CycleGan: python train.py --dataroot ./datasets/qrcode --name deblurLightCycleGAN_4block_e6 --model deblurQr_cycle_gan  --batch_size 1 --resize_or_crop scale_width_and_crop --loadSize 256 --fineSize 256 --netG mobilenet_5blocks --norm instance --expand_radio 6
- Pix2PixGan: python train.py --dataroot ./datasets/qrcode --name deblurPix2PixGAN --model deblurQr_pix2pix_gan  --batch_size 1 --resize_or_crop scale_width_and_crop --no_flip
- Test: python test.py --dataroot ./datasets/qrcode --name deblurPix2PixGAN --model deblurQr_pix2pix_gan  --batch_size 1 --resize_or_crop scale_width_and_crop --no_flip

## Future plan

1. 收集5000张最清晰的图，2000张距离模糊的图，2000张角度模糊的图。 => 标注数据集(wyt)
2. 训练鲁棒模型（loss下降图，acc上升图），保存checkpoint，留作最后在测试集上测试（每隔几个epoch画一个生成出来的二维码清晰度的图，挑最糊的效果好）、画图。（只保留Pix2PixGan，做的fancy一点即可）(lzn)
3. 解码时间（需要写个二维码decode的代码）、鲁棒性（极端距离和角度）、准确度比较（能在多少张图上work）。=>三种method最终我们胜出。(together)
4. xx的解码代码可能需要自己修改一下做到可以开源的地步。(xx)
5. PPT、论文。(together)



