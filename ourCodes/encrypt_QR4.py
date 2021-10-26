import cv2
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
from math import *
from scipy.interpolate import interp1d

###########################
# Periodic Functions
###########################
# Green Pixels
def p_g1_func(phase):
    return round(phase) % 2

# Red Pixels
def p_r1_func(phase):
    return phase

# Cos
def p1_func(phase):
    return 0.5 + 0.5 * cos(phase * 2)

# Exp
def p2_func(phase):
    return exp(2 * abs(1-fmod(phase/pi, 2)))/exp(2)

# Log
def p3_func(phase):
    return log(1+3*abs(1-fmod(phase/pi,2)))/log(4)

# Square
def p4_func(phase):
    return round(fmod(phase/2/pi,1));

# Triangle
def p5_func(phase):
    return abs(1-fmod(phase/pi,2))

###########################
# Phase Functions
###########################
# Green Pixels 1
def phi_g1_func(x, y):
    return x + y

# Green Pixels 2
def phi_g2_func(x, y):
    return floor((x-1)/2) + floor((y-1)/2)

# Red Pixels 1
def phi_r1_func(x, y):
    if fmod(x, 2) == 1 and fmod(y, 2) == 0:
        return 1
    else:
        return 0

# Red Pixels 2
def phi_r2_func(x, y):
    if fmod(x, 2) == 0 and fmod(y, 2) == 1:
        return 1
    else:
        return 0

# horizontal lines
def phi1_func(x, y):
    return x

# vertical lines
def phi2_func(x, y):
    return y

#####################################
## Compute inverse pm
#####################################
def pm_inverse(pm_x, pm, y):
    idx = np.argmin(abs(pm-y))
    idx = idx[1]

    ## interpolation
    if idx == 1 or idx == pm_x.shape[0]:
        phase = pm_x[idx]
    else:
        xx = pm_x[idx-1:idx+1]
        yy = pm[idx-1:idx+1]
        f1 = interp1d(yy, xx, kind='linear')
        phase = f1(y)
    return phase

#####################################
## Functions to blur boundary
#####################################

#####################################
## Add Fake Boundary for Camouflage
## @Input(Iencode): encoded QRcode image
## @Input(thr): the minimal distance between fake boundary (unit: pixel)
#####################################
def addFakeBoundary(Iencode, thr):
    Ifake = Iencode
    nrows = Iencode.shape[0]
    ncols = Iencode.shape[1]
    fake_rows = []
    fake_cols = []

    for xi in range(1, nrows-1):
        for yi in range(1, ncols-1):
            if Iencode[xi, yi] == Iencode[xi, yi+1]:
                ## Find a col with boundary
                if_gen_fake_col = 1
                if len(fake_cols) > 0:
                    if np.min(abs(np.array(fake_cols) - yi)) < thr:
                        if_gen_fake_col = 0

                ## Start to generate fake boundary
                if if_gen_fake_col == 1:
                    for xj in range(1, nrows):
                        Ifake[xj, yi+1] = Ifake[xj, yi]
                    fake_cols.append(yi)

            if Iencode[xi, yi] == Iencode[xi+1, yi]:
                ## Find a row with boundary
                if_gen_fake_row = 1
                if len(fake_rows) > 0:
                    if np.min(abs(np.array(fake_rows) - xi)) < thr:
                        if_gen_fake_row = 0

                ## Start to generate fake boundary
                if if_gen_fake_row == 1:
                    for yj in range(1, ncols):
                        Ifake[xi+1, yj] = Ifake[xi, yj]
                    fake_rows.append(xi)
    return Ifake

#####################################
## Add White Noise
## @Input(Iencode): encoded QR code image
## @Input(ratio): ratio of noise
#####################################
def addWhiteNoise(Iencode, ratio):
    Inoise = Iencode
    nrows = Iencode.shape[0]
    ncols = Iencode.shape[1]
    fake_rows = []
    fake_cols = []

    noise = np.random.rand(nrows, ncols)
    # idx = np.where()


if __name__ == "__main__":
    # Read QRCode Image
    filename = 'mbc19_qrcode.jpg'
    img = plt.imread(filename)

    # up-sampling (make image larger) and using only black white
    nrows = img.shape[0]
    ncols = img.shape[1]
    ratio = 2
    new_img = np.zeros((nrows*ratio, ncols*ratio))
    for xi in range(1, nrows):
        for yi in range(1, ncols):
            new_img[(xi-1)*ratio+1:xi*ratio, (yi-1)*ratio+1:yi*ratio] = img[xi, yi]
    img = new_img/255
    nrows = img.shape[0]
    ncols = img.shape[1]
    # plt.imshow(img)
    # plt.show()

    # Encode QRCode with Moire Pattern
    Iencode = np.zeros(img.shape)
    for xi in range(1, nrows):
        for yi in range(1, ncols):
            if img[xi, yi] > 0.5:
                Iencode[xi, yi] = p_g1_func(phi_g1_func(xi, yi))
            else:
                Iencode[xi, yi] = p_g1_func(phi_g1_func(xi, yi)+1)
    I2 = np.zeros((nrows, ncols, 3))
    I2[:, :, 2] = Iencode
    # plt.imshow(I2)
    # plt.show()

    ######################################
    ## Add Fake Boundary for Camouflage




