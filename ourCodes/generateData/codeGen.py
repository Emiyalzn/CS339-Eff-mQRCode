import os
import argparse
import cv2
import numpy as np
from encrypt import *
import qrcode

def genQRCode():
    num = 300
    for i in range(num):
        link = f'{i}'
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=0)
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f'../datasets/groundTruth/QR_{i}.jpg')
        qr.clear()

def getImagePathListFromRoot(root, shuffle=False):
    pathList = []
    for dirPath, dirNames, fileNames in os.walk(root):
        for file in fileNames:
            # print(file)
            if file.split('.')[-1].lower() in {'bmp','png','jpg','jpeg'}:
                imagePath = os.path.join(dirPath, file)
                pathList.append(imagePath)
    if shuffle:
        np.random.shuffle(pathList)
    print(pathList)
    return pathList

def getImages(root, num_figs):
    pathList = []
    for i in range(num_figs):
        imagePath = os.path.join(root, f"QR_{i}.jpg")
        pathList.append(imagePath)
    return pathList

def makeVideo():
    path = '../datasets/groundTruth'
    fileList = getImages(path, 100)
    # print(fileList)
    fps = 0.5
    size = (490, 490)
    video = cv2.VideoWriter("../datasets/mQRCodes_8%.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size, False)

    for item in fileList:
        if item.endswith('.jpg'):
            # print(item)
            image = encrypt(item)
            video.write(image)

    video.release()
    # cv2.destroyAllWindows()
    print('Video has been made.')

if __name__ == '__main__':
    makeVideo()
    # genQRCode()
