import numpy as np # gereklii kütüphaneler
import argparse
import imutils
import cv2

# komut argümanları kullanımı
ap =argparse.ArgumentParser()
ap.add_argument("-i","--image",help="image dosyasi yolu")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])

lower = np.array([0, 0, 0]) # siyah renk için lower ve upper değerleri
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(image, lower, upper)

cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, # konturleri buluyoruz
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("I found {} black shapes".format(len(cnts)))
cv2.imshow("Mask", shapeMask)
# konturler içinde geziniyoruz
for c in cnts:
	# konturleri çiziyoruz
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)