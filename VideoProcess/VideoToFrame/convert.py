#coding:utf-8

#from _typeshed import OpenBinaryMode
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread(r"C:\Users\INTE\CS339-Project\VideoProcess\VideoToFrame\cover\frame_4.jpg")
output = './afterprocess/'
print(img)
img_bright = cv.convertScaleAbs(img, alpha=1.5, beta=0)
print(img_bright)
cv.imwrite(output+'test.jpg',img_bright)
