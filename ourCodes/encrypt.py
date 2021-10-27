import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
from math import *
from scipy.interpolate import interp1d
import cv2

###########################
# Periodic Functions
###########################
# Green Pixels
def p_g1_func(phase):
    return fmod(round(phase), 2)

# Red Pixels
def p_r1_func(phase):
    return phase

# Cos
def p1_func(phase):
    return 0.5 + 0.5 * cos(phase * 2)

# Exp
def p2_func(phase):
    return exp(2 * abs(1 - fmod(phase / pi, 2))) / exp(2)

# Log
def p3_func(phase):
    return log(1 + 3 * abs(1 - fmod(phase / pi, 2))) / log(4)

# Square
def p4_func(phase):
    return round(fmod(phase / 2 / pi, 1))

# Triangle
def p5_func(phase):
    return abs(1 - fmod(phase / pi, 2))

###########################
# Phase Functions
###########################
# Green Pixels 1
def phi_g1_func(x, y):
    return x + y

# Green Pixels 2
def phi_g2_func(x, y):
    return floor((x - 1) / 2) + floor((y - 1) / 2)

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
    idx = np.argmin(abs(pm - y))
    idx = idx[1]

    ## interpolation
    if idx == 1 or idx == pm_x.shape[0]:
        phase = pm_x[idx]
    else:
        xx = pm_x[idx - 1:idx + 1]
        yy = pm[idx - 1:idx + 1]
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

    for xi in range(nrows-1):
        for yi in range(ncols-1):
            if Iencode[xi, yi] == Iencode[xi, yi + 1]:
                ## Find a col with boundary
                if_gen_fake_col = 1
                if len(fake_cols) > 0:
                    if np.min(abs(np.array(fake_cols) - yi)) < thr:
                        if_gen_fake_col = 0

                ## Start to generate fake boundary
                if if_gen_fake_col == 1:
                    for xj in range(nrows):
                        Ifake[xj, yi + 1] = Ifake[xj, yi]
                    fake_cols.append(yi)

            if Iencode[xi, yi] == Iencode[xi + 1, yi]:
                ## Find a row with boundary
                if_gen_fake_row = 1
                if len(fake_rows) > 0:
                    if np.min(abs(np.array(fake_rows) - xi)) < thr:
                        if_gen_fake_row = 0

                ## Start to generate fake boundary
                if if_gen_fake_row == 1:
                    for yj in range(ncols):
                        Ifake[xi + 1, yj] = Ifake[xi, yj]
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

    noise = np.random.rand(nrows, ncols)
    (idx, idy) = np.where(noise <= ratio)

    for i in range(idx.shape[0]):
        if Inoise[idx[i]][idy[i]] > 0.5:
            Inoise[idx[i]][idy[i]] = 0

    return Inoise

#####################################
## simulate the camera layer
## @INPUT(w): width of the camera
## @INPUT(h): height of the camera
#####################################
def simCameraLayer(h, w):
    Icamera = np.zeros((h, w))
    for xi in range(1, h):
        for yi in range(1, w):
            if (fmod(xi, 3) == 0 or fmod(xi, 3) == 1) and (fmod(yi, 3) == 0 or fmod(yi, 3) == 1):
                Icamera[xi, yi] = 1
            elif (fmod(xi, 3) == 0 or fmod(xi, 3) == 1) and (fmod(yi, 3) == 2):
                Icamera[xi, yi] = 0
            elif (fmod(xi, 3) == 2) and (fmod(yi, 3) == 0 or fmod(yi, 3) == 1):
                Icamera[xi, yi] = 0
            else:
                Icamera[xi, yi] = 1
    return Icamera

def checkRedPixels():
    nrows = 900
    ncols = 900
    I = np.zeros((nrows, ncols))
    for x in range(1, nrows):
        for y in range(1, ncols):
            if (x < nrows / 2 and y < ncols / 2) or (x >= nrows / 2 and y >= ncols / 2):
                I[x, y] = p_r1_func(phi_r1_func(x, y))
            else:
                I[x, y] = p_g1_func(phi_g1_func(x, y))
    plt.imshow(I)
    plt.show()

def encrypt(filename):
    # Read QRCode Image
    img = cv2.imread(filename, 0)
    # print(img)
    nrows = img.shape[0]
    ncols = img.shape[1]
    img = img / 255
    ratio = 1

    # up-sampling (make image larger) and using only black white
    # ratio = 2
    # new_img = np.zeros((nrows * ratio, ncols * ratio))
    # for xi in range(1, nrows):
    #     for yi in range(1, ncols):
    #         new_img[(xi - 1) * ratio + 1:xi * ratio, (yi - 1) * ratio + 1:yi * ratio] = img[xi, yi]
    # img = new_img / 255
    # nrows = img.shape[0]
    # ncols = img.shape[1]
    # plt.imshow(img, cmap='gray')
    # plt.show()

    # Encode QRCode with Moire Pattern
    Iencode = np.zeros(img.shape)
    for xi in range(img.shape[0]):
        for yi in range(img.shape[1]):
            if img[xi, yi] > 0.5:
                Iencode[xi, yi] = p_g1_func(phi_g1_func(xi, yi))
            else:
                Iencode[xi, yi] = p_g1_func(phi_g1_func(xi, yi) + 1)

    ######################################
    ## Add Fake Boundary for Camouflage
    Ifake = addFakeBoundary(Iencode, 200)

    ######################################
    ## Add white noise
    Inoise = addWhiteNoise(Ifake, 0.1)

    ## Leave the three locator
    # top left
    Inoise[0:7*10*ratio, 0:7*10*ratio] = img[0:7*10*ratio, 0:7*10*ratio]
    # top right
    Inoise[0:7*10*ratio, 22*10*ratio:29*10*ratio] = img[0:7*10*ratio, 22*10*ratio:29*10*ratio]
    # bottom left
    Inoise[22*10*ratio:29*10*ratio, 0:7*10*ratio] = img[22*10*ratio:29*10*ratio, 0:7*10*ratio]

    # Save Figures
    # cv2.imshow('Inoise', Inoise)
    # k = cv2.waitKey(0)
    # if k == ord('s'):
    #     cv2.imwrite('mqrcode.png', Inoise*255)
    # cv2.destroyAllWindows()

    return (Inoise*255).astype(np.uint8)

if __name__ == '__main__':
    encrypt('mbc19_qrcode.jpg')