import numpy as np
import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

for angle in np.arange(0, 360, 15): # 0 dan 360 a 15 ilerleyerek açı değerlerini gezdik
	rotated = imutils.rotate(image, angle) # rotate komutu ile ersmi döndürdük
	cv2.imshow("Rotated (Problematic)", rotated)
	cv2.waitKey(0)
# aynı kesilmemiş penceredeki hali
for angle in np.arange(0, 360, 15):
	rotated = imutils.rotate_bound(image, angle)
	cv2.imshow("Rotated (Correct)", rotated)
	cv2.waitKey(0)

# iutils.rotate_bound arkasındaki çalışma mantığı
def rotate_bound(image, angle):
    
    (h, w) = image.shape[:2] # görüntünün boyutlarını alır
    (cX, cY) = (w // 2, h // 2) # görüntünün merkezini belirler
    
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)# dönme matrisi
    cos = np.abs(M[0, 0])# matristen cos ve sin değerleri alınır
    sin = np.abs(M[0, 1])
    
    nW = int((h * sin) + (w * cos))# yeni genişlik ve yükseklik hesaplanır
    nH = int((h * cos) + (w * sin))
    
    M[0, 2] += (nW / 2) - cX # dönüş matrisi değiştirilir
    M[1, 2] += (nH / 2) - cY
   
    return cv2.warpAffine(image, M, (nW, nH)) # yeni görüntü döndürülür

cv2.imshow("image",rotate_bound(image,45))
cv2.waitKey(0)



