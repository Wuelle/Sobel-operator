import math 
import numpy as np
import cv2
import colorsys
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

img = cv2.imread("TestImage.jpg")
result = np.zeros([img.shape[0], img.shape[1], 3])

def SetPixel(coords, color):
	global img
	result[coords[0], coords[1], 0] = color[2]
	result[coords[0], coords[1], 1] = color[1]
	result[coords[0], coords[1], 2] = color[0]

def GetPixelValue(x, y):
	#Pixels outside the image are returned as black
	try: 
		return np.average(img[x, y])
	except:
		return 0

def ApplyFilter(x, y):
	Y_Kernel_Value = 0
	Y_Kernel_Value +=  1 * GetPixelValue(x-1, y-1)
	Y_Kernel_Value +=  2 * GetPixelValue(x-1, y)
	Y_Kernel_Value +=  1 * GetPixelValue(x-1, y+1)
	Y_Kernel_Value += -1 * GetPixelValue(x+1, y-1)
	Y_Kernel_Value += -2 * GetPixelValue(x+1, y)
	Y_Kernel_Value += -1 * GetPixelValue(x+1, y+1)

	X_Kernel_Value = 0
	X_Kernel_Value +=  1 * GetPixelValue(x-1, y-1)
	X_Kernel_Value +=  2 * GetPixelValue(x, y-1)
	X_Kernel_Value +=  1 * GetPixelValue(x+1, y-1)
	X_Kernel_Value += -1 * GetPixelValue(x-1, y+1)
	X_Kernel_Value += -2 * GetPixelValue(x, y+1)
	X_Kernel_Value += -1 * GetPixelValue(x+1, y+1)

	return math.atan2(Y_Kernel_Value, X_Kernel_Value),math.sqrt(X_Kernel_Value**2+Y_Kernel_Value**2)

#Calculate all the pixel values for the 'result' image
for x in range(img.shape[0]):
	for y in range(img.shape[1]):
		angle, value = ApplyFilter(x, y)
		rgb_color = colorsys.hsv_to_rgb(angle, 1, value/(math.sqrt(2)*255))
		SetPixel([x, y], rgb_color)

if img.shape[0] > img.shape[1]:
	result_conc = np.concatenate((img/255, result), axis=1)
else: 
	result_conc = np.concatenate((img/255, result), axis=0)

cv2.imwrite("Result.jpg", result*255)
cv2.imshow("Result", result_conc)
cv2.waitKey()
