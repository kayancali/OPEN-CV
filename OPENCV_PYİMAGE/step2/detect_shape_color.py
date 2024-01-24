
# gerekli kütüphaneler ve farklı dosyalardaki kodları çağırma işlemi

from claslar.shapedetector import ShapeDetector
from claslar.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
# terminal kullanımı için argparse kütüphanesi kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)# yeniden boyutlandırma
ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (5, 5), 0)# bulur uygulama
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)# gri tonlara çevirme
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)# bgr dan lab formuna çevirme
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]# threshold uygulama

# konturları bulma
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# diğer dosyadaki şekil ve renk bulma kudlarını kullanmak için atama işlemi
sd = ShapeDetector()
cl = ColorLabeler()

for c in cnts:# konturların içinde gezme
	
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)# konturların merkezini bulma
	cY = int((M["m01"] / M["m00"]) * ratio)
	
	shape = sd.detect(c)# şekilleri tespit etmek 
	color = cl.label(lab, c)# renkleri tespit etmek
	
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	text = "{} {}".format(color, shape)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)# konturların kenarlarını çizmek
	cv2.putText(image, text, (cX, cY),# şekillerin ismini ve rengini yazmak
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	# imshow 
	cv2.imshow("Image", image)
	cv2.waitKey(0)