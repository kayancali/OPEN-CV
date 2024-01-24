# kütüphaneler
import numpy as np
import argparse
import imutils
import cv2
# komut argümanları 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# resmi gri tonlara çevirme
gray = cv2.GaussianBlur(gray, (3, 3), 0) # bulanıklaştırma
edged = cv2.Canny(gray, 20, 100)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,# resmin konturlarınnı bulma
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# en büyük konturu bulma ve bir mask uygulama
if len(cnts) > 0:
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(gray.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1) # kontur çizme
	
    # en büyük konturun sınırlarını belirleme
	(x, y, w, h) = cv2.boundingRect(c)
	imageROI = image[y:y + h, x:x + w]
	maskROI = mask[y:y + h, x:x + w]
	imageROI = cv2.bitwise_and(imageROI, imageROI,
		mask=maskROI)

# imutils ile dönrüme işlemlerini uygulama	
for angle in np.arange(0, 360, 15):
    rotated = imutils.rotate(imageROI, angle)
    cv2.imshow("Rotated (Problematic)", rotated)
    cv2.waitKey(0)

for angle in np.arange(0, 360, 15):
    rotated = imutils.rotate_bound(imageROI, angle)
    cv2.imshow("Rotated (Correct)", rotated)
    cv2.waitKey(0)