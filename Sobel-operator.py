import math 
import numpy as np
import cv2
import colorsys
import sys
"""
The Algorithm:
	-https://www.youtube.com/watch?v=uihBwtPIBxM
Vertical Kernel:
1  0 -1
2  0 -2
1  0 -1
Horizontal Kernel:
 1  2  1
 0  0  0
-1 -2 -1
"""

img_raw = cv2.imread(sys.argv[1])

#Add padding to the image
img = np.zeros([img_raw.shape[0]+2, img_raw.shape[1]+2, img_raw.shape[2]])
img[1:img_raw.shape[0]+1, 1:img_raw.shape[1]+1,] = img_raw


result = np.zeros([img_raw.shape[0], img_raw.shape[1], 3])

def ApplyFilter(x, y):
	img_part = np.average(img[x-1:x+2, y-1:y+2], axis = 2)
	y_kernel = np.array([
		[1, 0, -1],
		[2, 0, -2],
		[1, 0, -1]])

	x_kernel = np.array([
		[ 1,  2,  1],
		[ 0,  0,  0],
		[-1, -2, -1]])

	Y_Kernel_Value = np.dot(y_kernel.flatten(), img_part.flatten())
	X_Kernel_Value = np.dot(x_kernel.flatten(), img_part.flatten())

	return math.atan2(Y_Kernel_Value, X_Kernel_Value),math.sqrt(X_Kernel_Value**2+Y_Kernel_Value**2)

#Calculate all the pixel values for the 'result' image
for x in range(1, img.shape[0]-1):
	for y in range(1, img.shape[1]-1):
		angle, value = ApplyFilter(x, y)
		rgb_color = colorsys.hsv_to_rgb(angle, 1, value/(math.sqrt(2)*255))
		result[x-1, y-1] = rgb_color


if img.shape[0] > img.shape[1]:
	result_conc = np.concatenate((img_raw/255, result), axis=1)
else: 
	result_conc = np.concatenate((img_raw/255, result), axis=0)

cv2.imwrite(sys.argv[2], result*255)
cv2.imshow("Result", result_conc)
cv2.waitKey()
