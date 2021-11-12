import cv2 as cv
import numpy as np
import glob

i = 0
for jpgfile in glob.glob(r'C:\Users\INTE\CS339-Project\VideoProcess\VideoToFrame\cover\*.jpg'):
    img_org = cv.imread(jpgfile)

    # hls分量拆分
    hls = cv.cvtColor(img_org, cv.COLOR_BGR2HLS)
    g_hls_h = hls[:, :, 0]
    g_hls_l = hls[:, :, 1]
    g_hls_s = hls[:, :, 2]

    # h分量
    hls_hf = g_hls_h.astype(np.float)
    hls_hf += 8
    hls_hf[hls_hf > 180] -= 180  # 超过180
    hls_hf[hls_hf < 0] += 180  # 小于0
    new_hls_h = hls_hf.astype("uint8")

    # l分量
    hls_lf = g_hls_l.astype(np.float)
    hls_lf += 37
    hls_lf[hls_lf < 0] = 0
    hls_lf[hls_lf > 255] = 255
    new_hls_l = hls_lf.astype("uint8")

    # s分量
    hls_ls = g_hls_s.astype(np.float)
    hls_ls += 69
    hls_ls[hls_ls < 0] = 0
    hls_ls[hls_ls > 255] = 255
    new_hls_s = hls_ls.astype("uint8")

    # 重新组合新图片 并转换成BGR图片
    new_bgr = cv.cvtColor(cv.merge([new_hls_h, new_hls_l, new_hls_s]), cv.COLOR_HLS2BGR)
    cv.imwrite('./afterprocess/{}.jpg'.format(i), new_bgr)
    i = i + 1