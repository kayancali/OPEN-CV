from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])# görüntüyü terminalden aldık
ratio = image.shape[0] / 500.0# görüntü yükseklğini 500 e böldük
orig = image.copy()# görüntüyü kopyaladık
image = imutils.resize(image, height = 500)# yeniden boyutlandırdık

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# graye çevirdik
gray = cv2.GaussianBlur(gray, (5, 5), 0)# blur uyguladık
edged = cv2.Canny(gray, 75, 200)#  köşelerini saptadık

# konturları bulduk
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# kare olan konturu bulmak için döngü başlattık
for c in cnts:

	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	if len(approx) == 4:
		screenCnt = approx
		break
#çarpıklığı önleyip karşıdan bakılan bir perspektif görüntüsü elde ederiz
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)# tekrar gri formata çevirdik
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

# orjinal ve transfer alini ekrana bastık

cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
cv2.destroyAllwindows()


