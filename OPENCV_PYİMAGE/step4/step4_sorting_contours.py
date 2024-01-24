
# gerkli kütüphaneler
import numpy as np
import argparse
import imutils
import cv2

# soldan  sağa sıralama fonksiyonu
def sort_contours(cnts, method="left-to-right"):
	reverse = False
	i = 0
	
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True

	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	
	return (cnts, boundingBoxes)

def draw_contour(image, c, i):
	
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	
	cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (255, 255, 255), 2)

	return image
# terminalden argüman girişi için argaparse küytüphanesi kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
#image görüntüsünün ilk 2 boyutunda bir mask uyguluyoruz
accumEdged = np.zeros(image.shape[:2], dtype="uint8")

for chan in cv2.split(image):
    # düngüden gelen görüntülere blur uyguluyoruz
	chan = cv2.medianBlur(chan, 11)
	edged = cv2.Canny(chan, 50, 200)
	accumEdged = cv2.bitwise_or(accumEdged, edged)



# konturleri buluyoruz
cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
 #alanları büyükten küçüğe sıralıyoruz ve ilk 5 değerini döndürüyoruz
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
orig = image.copy()

for (i, c) in enumerate(cnts):
	orig = draw_contour(orig, c, i)



(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])

for (i, c) in enumerate(cnts):
	draw_contour(image, c, i)

# son görüntüleri gösteriyoruz

cv2.imshow("Edge Map", accumEdged)	
cv2.imshow("Unsorted", orig)
cv2.imshow("Sorted", image)
cv2.waitKey(0)