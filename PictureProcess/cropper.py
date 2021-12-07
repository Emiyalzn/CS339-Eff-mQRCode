import numpy as np
from PIL import Image
import cv2
import os
import math
import copy

from numpy.core.fromnumeric import resize

np.set_printoptions(threshold=np.inf)

# get image from the folder
def openimage(path):
	files = os.listdir(path)
	img_list = {}
	for pic in files:
		if pic[-3:] == 'jpg':
			image = cv2.imread(path+pic)
			# image = cv2.blur(image,(8,8))
			img_list[pic] = image
			# cv2.imshow('ImageWindow', image)
			# cv2.waitKey()

	return img_list

# check area of contour and child contours
def check_contours_area_1(contour1, contour2):
	contour1_area = cv2.contourArea(contour1)
	contour2_area = cv2.contourArea(contour2)
	if contour2_area == 0:
		return False
	area_ratio = contour1_area / contour2_area
	if area_ratio > 1.0:
		return True  # external
	return False


def check_contours_area_2(contour1, contour2):
	contour1_area = cv2.contourArea(contour1)
	contour2_area = cv2.contourArea(contour2)
	if contour2_area == 0:
		return False
	area_ratio = contour1_area / contour2_area
	# print('area ratio 2 = ', area_ratio)
	if area_ratio > 1.0:
		return True  # internal
	return False

# find center of contour
def compute_center(contour):
	M = cv2.moments(contour)
	x = int(M['m10'] / M['m00'])
	y = int(M['m01'] / M['m00'])
	return x, y

def check_contours_center(x0, y0, x1, y1, x2, y2):
	distance0 = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
	distance1 = math.sqrt((x0 - x2) ** 2 + (y0 - y2) ** 2)
	distance2 = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
	# print('distance0 =', distance0)
	# print('distance1 =', distance1)
	# print('distance2 =', distance2)
	if (distance0 + distance1 + distance2)/3 < 5:
	# if (distance0 < 5):
		return True
	return False

def proc_img(img):
	#_,gray=cv2.threshold(img,0,260,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)  #convert to binary image
	image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	image = cv2.blur(image,(10,10))
	#_,gray=cv2.threshold(image,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
	gray = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	contours,hierachy=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	# cv2.drawContours(gray,contours,-1,(128,255,0),3)
	# cv2.imshow("Keypoints", gray)
	# cv2.waitKey(0)
	hierachy = hierachy[0]
	#print(hierachy)
	centers = []
	res = np.array([])
	test = copy.deepcopy(img)
	for i in range(len(hierachy)):
		#cv2.drawContours(gray,contours[i],-1,(128,255,0),3)
		#cv2.imshow("partcontours", gray)
		#cv2.waitKey(10)
		child = hierachy[i][2]
		# print('child =', child)
		# cv2.drawContours(gray,contours[i],-1,(128,255,0),3)
		# cv2.imshow("Keypoints", gray)
		# # cv2.destroyAllWindows()
		# cv2.waitKey(0)
		# if child != -1:
		# 	print('father =', i)
		# 	print('child =', child)
		# 	print('grandchild =', hierachy[child][2])
		if child != -1 and hierachy[child][2] != -1 and hierachy[hierachy[child][2]][2] != -1:
			#print('Is there any?')
			grandchild = hierachy[child][2]
			if check_contours_area_1(contours[i], contours[child]) == True and check_contours_area_2(contours[child], contours[grandchild]) == True:
				#print("Checked?")
				x_self,y_self = compute_center(contours[i])
				x_child,y_child = compute_center(contours[child])
				x_grandchild,y_grandchild = compute_center(contours[grandchild])
				if check_contours_center(x_self,y_self,x_child,y_child,x_grandchild,y_grandchild) == True:
					centers.append([x_self,y_self,i])
					for j in range(100):
						test[y_self+j,x_self+j] = [0,0,255]
	print('centers =', centers)

	cv2.imshow("test",test)
	cv2.waitKey(0)

	if len(centers)<3:
		return res
	
	max_distance = 0
	for i in range(len(centers)):
		for j in range(i+1, len(centers)):
			for k in range(j+1, len(centers)):
				distance0 = math.sqrt((centers[i][0] - centers[j][0]) ** 2 + (centers[i][1] - centers[j][1]) ** 2)
				distance1 = math.sqrt((centers[i][0] - centers[k][0]) ** 2 + (centers[i][1] - centers[k][1]) ** 2)
				distance2 = math.sqrt((centers[j][0] - centers[k][0]) ** 2 + (centers[j][1] - centers[k][1]) ** 2)
				if abs(distance0 - distance1) < 5:
					if abs(distance0**2 + distance1**2 - distance2**2) < (distance0**2 + distance1**2)/100:
						if distance0 >= max_distance:
							max_distance = distance0
							res = np.concatenate((contours[centers[i][2]], contours[centers[j][2]], contours[centers[k][2]]))
				elif abs(distance0 - distance2) < 5:
					if abs(distance0**2 + distance2**2 - distance1**2) < (distance0**2 + distance1**2)/100:
						if distance0 >= max_distance:
							max_distance = distance0
							res = np.concatenate((contours[centers[i][2]], contours[centers[j][2]], contours[centers[k][2]]))
				elif abs(distance1 - distance2) < 5:
					if abs(distance1**2 + distance2**2 - distance0**2) < (distance0**2 + distance1**2)/100:
						if distance1 >= max_distance:
							max_distance = distance1
							res = np.concatenate((contours[centers[i][2]], contours[centers[j][2]], contours[centers[k][2]]))
	return res

def get_qrcode_and_type(img, raw, flag):
	contours = proc_img(img)
	result = np.array([])
	if contours.size != 0:
		rect = cv2.minAreaRect(contours)
		#contour_areas = []
		#for contour in contours:
		#	contour_areas.append(cv2.contourArea(contour))

		#contour_area = max(contour_areas)
		#total_area = (np.max(box[:,1]) - np.max(box[:,1])) * (np.max(box[:,0]) - np.min(box[:,0]))
		
		#area_ratio = contour_area - total_area

		box = cv2.boxPoints(rect)
		box = np.int0(box)
		#print('box = ', box)
		result=copy.deepcopy(raw)
		#print(np.max(box[:,1]) - np.min(box[:,1]))
		# if flag :
		# 	if (np.max(box[:,1]) - np.min(box[:,1]) > 500):
		# 		return np.array([])
		print(np.min(box[:,1]) - 15)
		print(np.max(box[:,1]) + 15)
		print(np.min(box[:,0]) - 15)
		print(np.max(box[:,0]) + 15)
		result = raw[np.min(box[:,1]) - 15 : np.max(box[:,1] + 15), np.min(box[:,0]) - 15:np.max(box[:,0]) + 15]
		#cv2.drawContours(result, [box], 0, (255, 128, 255), 2)
		#cv2.drawContours(img,[contours[0]],0,(0, 125, 255),2)
		#cv2.drawContours(img,[contours[1]],0,(0, 120, 255),2)
		#cv2.drawContours(img,[contours[2]],0,(0, 120, 255),2)
		#print(contours[0])
		#cv2.imshow('img',result)
		#cv2.waitKey(1)
		#cv2.imshow('img',result)
		#cv2.waitKey(1)
		#cv2.imwrite('./saved/'+str(1)+'.png',result)

	#if result.size != 0:
	#	gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
	#	_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
	#	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	#	cnt = contours[0]
	#	x,y,w,h = cv2.boundingRect(cnt)
	#	result = result[y:y+h,x:x+w]
	return result

img_list = openimage("./experiment/ang_10/")
qr_list = {}
index = 1
for img_key in img_list:
	img = img_list[img_key]
	#img_norm=cv2.normalize(img,dst=None,alpha=350,beta=10,norm_type=cv2.NORM_MINMAX)
	# if you want to enlarge the contrast of image to crop more, uncommon the next line
	# img = cv2.convertScaleAbs(img,alpha=1.5,beta=0)
	#cv2.imwrite('./norm/'+img_key,img_norm)
	qr_img = get_qrcode_and_type(img, img, 1)
	#qr_img2 = get_qrcode_and_type(img, img, 0)
	if qr_img.size != 0:
		#qr_img=cv2.cvtColor(qr_img,cv2.COLOR_BGR2GRAY)
		#_,qr_img=cv2.threshold(qr_img,140,255,cv2.THRESH_BINARY)  #convert to binary
		qr_img = cv2.resize(qr_img, (580,580))
		qr_img = qr_img[5:575, 5:575]
		qr_img = cv2.resize(qr_img, (290,290))
		cv2.imshow('raw',qr_img)
		cv2.waitKey(1)
		cv2.imwrite('./semi/ang_10/'+img_key, qr_img)