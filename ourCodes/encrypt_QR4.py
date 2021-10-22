import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read QRCode Image
filename = 'mbc19_qrcode.jpg'
img = plt.imread(filename)

# up-sampling (make image larger) and using only black white
nrows = img.shape[0]
ncols = img.shape[1]
ratio = 2
new_img = np.zeros(nrows*ratio, ncols*ratio)
