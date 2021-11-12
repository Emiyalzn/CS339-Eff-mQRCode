import cv2 as cv
import numpy as np

# 全局变量
g_hls_h = []  # 图片分量 hls
g_hls_l = []
g_hls_s = []
# 滑动设置值
g_diff_h, g_diff_l, g_diff_s = 0, 0, 0


# 修改图片各分量 组合成新图片
def change_hls():
    global g_hls_h, g_hls_l, g_hls_s, g_diff_h, g_diff_l, g_diff_s

    # h分量
    hls_hf = g_hls_h.astype(np.float)
    hls_hf += g_diff_h
    hls_hf[hls_hf > 180] -= 180  # 超过180
    hls_hf[hls_hf < 0] += 180  # 小于0
    new_hls_h = hls_hf.astype("uint8")

    # l分量
    hls_lf = g_hls_l.astype(np.float)
    hls_lf += g_diff_l
    hls_lf[hls_lf < 0] = 0
    hls_lf[hls_lf > 255] = 255
    new_hls_l = hls_lf.astype("uint8")

    # s分量
    hls_ls = g_hls_s.astype(np.float)
    hls_ls += g_diff_s
    hls_ls[hls_ls < 0] = 0
    hls_ls[hls_ls > 255] = 255
    new_hls_s = hls_ls.astype("uint8")

    # 重新组合新图片 并转换成BGR图片
    new_bgr = cv.cvtColor(cv.merge([new_hls_h, new_hls_l, new_hls_s]), cv.COLOR_HLS2BGR)

    cv.imshow("image", new_bgr)


# h分量 值修改
def on_value_h(a):
    global g_diff_h
    value = cv.getTrackbarPos("value_h", "image")
    value = (value - 180)
    g_diff_h = value
    change_hls()


# l分量 值修改
def on_value_l(a):
    global g_diff_l
    value = cv.getTrackbarPos("value_l", "image") * 2
    value -= 255
    g_diff_l = value
    change_hls()


# s分量 值修改
def on_value_s(a):
    global g_diff_s
    value = cv.getTrackbarPos("value_s", "image") * 2
    value -= 255
    g_diff_s = value
    change_hls()


def main():
    global g_hls_h, g_hls_l, g_hls_s
    # 加载图片
    img_org = cv.imread("./cover/frame_4.jpg")

    # hls分量拆分
    hls = cv.cvtColor(img_org, cv.COLOR_BGR2HLS)
    g_hls_h = hls[:, :, 0]
    g_hls_l = hls[:, :, 1]
    g_hls_s = hls[:, :, 2]

    print(img_org.shape)

    # 滑动条创建、设置初始值
    cv.namedWindow("image")
    cv.createTrackbar("value_h", "image", 0, 360, on_value_h)
    cv.createTrackbar("value_l", "image", 0, 255, on_value_l)
    cv.createTrackbar("value_s", "image", 0, 255, on_value_s)
    cv.setTrackbarPos("value_h", "image", 180)
    cv.setTrackbarPos("value_l", "image", 127)
    cv.setTrackbarPos("value_s", "image", 127)

    # 退出
    while True:
        key = cv.waitKey(50) & 0xFF
        if key == 27:  # 退出
            break

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
