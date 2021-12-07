import numpy as np
from PIL import Image
import cv2
import os
import math
import copy

np.set_printoptions(threshold=np.inf)

# get image
def openimage(path):
    files = os.listdir(path)
    img_list = {}
    i = 1
    for pic in files:
        if pic[-3:] == 'png':
            image = cv2.imread(path+pic)
            img_list[pic] = image
            #cv2.imshow('ImageWindow', image)
            # cv2.waitKey()
        i += 1
        if i > 50:
            break

    return img_list

def label_pixel(bw_img, row, col):
    res = set()
    l = []
    l.append((row, col))
    # print(row,col)
    while len(l) != 0:
        # print(res)
        pixel = l.pop()
        if (pixel in res) == False:
            res.add(pixel)

        i = pixel[0]
        j = pixel[1]

        if i > 0 and bw_img[i-1][j] != 127 and ((i-1, j) in res) == False:
            l.append((i-1, j))

        if i < 28 and bw_img[i+1][j] != 127 and ((i+1, j) in res) == False:
            l.append((i+1, j))

        if j > 0 and bw_img[i][j-1] != 127 and ((i, j-1) in res) == False:
            l.append((i, j-1))

        if j < 28 and bw_img[i][j+1] != 127 and ((i, j+1) in res) == False:
            l.append((i, j+1))

        if i > 0 and j > 0 and bw_img[i-1][j-1] != 127 and ((i-1, j-1) in res) == False:
            l.append((i-1, j-1))

        if i < 28 and j < 28 and bw_img[i+1][j+1] != 127 and ((i+1, j+1) in res) == False:
            l.append((i+1, j+1))

        if i > 0 and j < 28 and bw_img[i-1][j+1] != 127 and ((i-1, j+1) in res) == False:
            l.append((i-1, j+1))

        if i < 28 and j > 0 and bw_img[i+1][j-1] != 127 and ((i+1, j-1) in res) == False:
            l.append((i+1, j-1))

    return res

def decode_bw_list(black_white_list):
    res = np.ones([29, 29]) * 127
    overall_labels_map = {}
    max_overall_label = 1

    res[0:7, 0:7] = 255
    res[0:7, -7:] = 255
    res[-7:, 0:7] = 255

    res[0:7, 0] = 0
    res[0:7, 6] = 0
    res[0:7, -1] = 0
    res[0:7, -7] = 0

    res[0, 0:7] = 0
    res[0, -7:] = 0
    res[6, 0:7] = 0
    res[6, -7:] = 0

    res[-7:, 0] = 0
    res[-7:, 6] = 0
    res[-7, 0:7] = 0
    res[-1, 0:7] = 0

    res[2:5, 2:5] = 0
    res[2:5, -5:-2] = 0
    res[-5:-2, 2:5] = 0

    for bw_img in black_white_list:

        labels = np.zeros([29, 29])
        label_pixel_map = {}
        max_index = 1
        for i in range(29):   # Assign labels
            for j in range(29):
                if bw_img[i][j] != 127 and labels[i][j] == 0:
                    same_label_set = label_pixel(bw_img, i, j)
                    label_pixel_map[max_index] = copy.deepcopy(same_label_set)
                    for point in same_label_set:
                        labels[point[0]][point[1]] = max_index
                    max_index += 1

        for incoming_label in label_pixel_map:
            union_set = label_pixel_map[incoming_label]
            for pixel in union_set:
                if res[pixel[0]][pixel[1]] == 127:
                    res[pixel[0]][pixel[1]] = bw_img[pixel[0]][pixel[1]]
            tmp_label_set = set()
            for current_label in overall_labels_map:
                if union_set.isdisjoint(overall_labels_map[current_label]) == False:
                    intersection = union_set.intersection(
                        overall_labels_map[current_label])
                    point = intersection.pop()

                    if bw_img[point[0]][point[1]] != res[point[0]][point[1]]:
                        # print(point)
                        for pixel in overall_labels_map[current_label]:
                            # print(pixel)
                            # print(res[pixel[0]][pixel[1]])
                            res[pixel[0]][pixel[1]] = abs(
                                res[pixel[0]][pixel[1]] - 255)
                            # print(res[pixel[0]][pixel[1]])

                    tmp_label_set.add(current_label)
                    union_set = union_set.union(copy.deepcopy(
                        overall_labels_map[current_label]))

            if len(tmp_label_set) != 0:
                for label in tmp_label_set:
                    overall_labels_map.pop(label)

            if incoming_label not in overall_labels_map:
                overall_labels_map[incoming_label] = union_set
            else:
                if overall_labels_map[incoming_label].issubset(union_set):
                    pass
                else:
                    max_overall_label = 0
                    for label in overall_labels_map:
                        if label > max_overall_label:
                            max_overall_label = label
                    max_overall_label += 1

                    overall_labels_map[max_overall_label] = overall_labels_map.pop(
                        incoming_label)
                    overall_labels_map[incoming_label] = copy.deepcopy(
                        union_set)


        if (127 in res) == False:
            if res[7, 0] == 0:
                for i in range(29):
                    for j in range(29):
                        # upper left locator and upper right
                        if i <= 6 and (j <= 6 or (j >= 22 and j <= 28)):
                            continue
                        if (i >= 22 and i <= 28) and j <= 6:  # lower left
                            continue
                        res[i][j] = abs(res[i][j] - 255)

            return res

    if res[7, 0] == 0:
        for i in range(29):
            for j in range(29):
                # upper left locator and upper right
                if i <= 6 and (j <= 6 or (j >= 22 and j <= 28)):
                    continue
                if (i >= 22 and i <= 28) and j <= 6:  # lower left
                    continue
                res[i][j] = abs(res[i][j] - 255)
    return res

def preprocess(qr_list):
    res = np.ones([29, 29]) * 255
    res[0:7, 0] = 0
    res[0:7, 6] = 0
    res[0:7, -1] = 0
    res[0:7, -7] = 0

    res[0, 0:7] = 0
    res[0, -7:] = 0
    res[6, 0:7] = 0
    res[6, -7:] = 0

    res[-7:, 0] = 0
    res[-7:, 6] = 0
    res[-7, 0:7] = 0
    res[-1, 0:7] = 0

    res[2:5, 2:5] = 0
    res[2:5, -5:-2] = 0
    res[-5:-2, 2:5] = 0

    cnt = 0
    black_white_list = []
    for qr_key in qr_list:
        qr_img = qr_list[qr_key]
        black_white = np.ones([29, 29]) * 127

        index = np.zeros([29, 29])
        #print("qr_img:", qr_img)

        for i in range(29):
            for j in range(29):
                # upper left locator and upper right
                if i <= 6 and (j <= 6 or (j >= 22 and j <= 28)):
                    continue
                if (i >= 22 and i <= 28) and j <= 6:  # lower left
                    continue
                block = qr_img[i*20:(i+1)*20, j*20:(j+1)*20]
                # print("block:",block)
                count_black = 0
                count_white = 0
                for m in range(20):
                    for n in range(20):
                        if block[m][n] == 0:
                            count_black += 1
                        elif block[m][n] == 255:
                            count_white += 1

                if count_black / 400 >= 0.5:
                    black_white[i, j] = 0
                elif count_white / 400 >= 0.3:
                    black_white[i, j] = 255
    

        black_white[0:7, 0:7] = 127
        black_white[0:7, -7:] = 127
        black_white[-7:, 0:7] = 127

        black_white_list.append(black_white)

        #cv2.imshow("bw", np.uint8(black_white))
        #cv2.waitKey(1)
        print(qr_key)
        #print(cv2.imwrite('./inspection/'+qr_key, black_white))
        cnt += 1

    return black_white_list

img_list = openimage("./inspection/")
qr_list = {}
index = 1
for img_key in img_list:
    qr_img = img_list[img_key]

    if qr_img.size != 0:

        mask1 = cv2.inRange(qr_img, (0, 0, 0), (255, 140, 255))
        mask2 = cv2.inRange(qr_img, (150, 0, 0), (255, 255, 255))
        mask3 = cv2.inRange(qr_img, (0, 0, 200), (255, 255, 255))

        img1 = cv2.bitwise_or(mask1, mask2, mask3) / 2

        img2 = cv2.inRange(qr_img, (170, 0, 170), (255, 100, 255))

        # img1: Black is green, white is others
        # img2: White is purple, black is others
        # How can I merge these imgs????????

        #img1 = cv2.bitwise_and(qr_img,qr_img, mask=mask)

        qr_img = img1 + img2/2
        #cv2.imshow('img', np.uint8(qr_img))
        #cv2.waitKey(1)
        #cv2.imwrite('./saved/QR0/'+img_key, qr_img)
        qr_list[img_key] = qr_img
        index += 1

black_white_list = preprocess(qr_list)
final_res = decode_bw_list(black_white_list)

#cv2.imshow('img', final_res)
#cv2.waitKey(1)
cv2.imwrite('./saved/QR0/final_res.png', final_res)

