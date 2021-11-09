from traceback import format_exc
import cv2
from pathlib import Path
from PIL import Image

import numpy as np


def ImageToMatrix(file):
    im = Image.open(file)
    width, height = im.size
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data, dtype='float') / 255.0

    new_data = np.reshape(data, (height, width))
    return new_data


def Brenner(img):
    x, y = img.shape
    D = 0
    for i in range(x - 2):
        for j in range(y - 2):
            D += (img[i + 2, j] - img[i, j]) ** 2
    return D


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def main(input_path):
    for file in Path(input_path).rglob("*.jpg"):
        # 拉普拉斯算子
        image = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        # Brenner 检测
        frame = ImageToMatrix(file)
        score = Brenner(frame)
        print(fm, score)

if __name__ == '__main__':
    print("Start...")
    input_Folder = './orgin/'
    #output_Folder = r"D:\SJTU Courses\3-1\sources\result"
    try:
        main(input_Folder)
        print("finished")
    except Exception as err:
        print(f"程序运行失败！！！请联系数据处理中心:{err}")
        print(format_exc())
    input("按任意键盘退出!!!")