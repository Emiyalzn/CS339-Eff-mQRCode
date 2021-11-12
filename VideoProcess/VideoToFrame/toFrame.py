import cv2

# Opens the Video file
pic_path = './frames/'
cap = cv2.VideoCapture('video.mp4')
i = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    tmp_path = pic_path + 'frame' + str(i) + '.jpg'
    cv2.imwrite(tmp_path, frame)
    i += 1

cap.release()
cv2.destroyAllWindows()