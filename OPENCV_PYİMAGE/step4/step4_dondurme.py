import numpy as np
import argparse
import imutils
import cv2
# kütüphanelerin eklenmesi ve komut satırı kullanmak için tanımlamalar
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # fotoğrafın komut satırından alınması

for angle in np.arange(0, 360, 15): # 15 derece açı ile döndürme işlemi
	rotated = imutils.rotate(image, angle)
	cv2.imshow("Rotated (Problematic)", rotated)
	cv2.waitKey(0)

for angle in np.arange(0, 360, 15):# döndürme işlemini kırpmadan yapma
	rotated = imutils.rotate_bound(image, angle)
	cv2.imshow("Rotated (Correct)", rotated)
	cv2.waitKey(0)