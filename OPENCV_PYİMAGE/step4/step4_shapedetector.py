

import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])


# şekillerin ne olduğunu bulmak için fonks.
def detect(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
    if len(approx) == 3:
        shape = "triangle"
  
    elif len(approx) == 4:
       
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    
    elif len(approx) == 5:
        shape = "pentagon"
    
    else:
        shape = "circle"
   
    return shape
# resmi yeniden boyutlandırma
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])# resmin 0. notası

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)# resmi gri tonlara çevirme
blurred = cv2.GaussianBlur(gray, (5, 5), 0)# blur uygulama
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]# thresold uygulama
# konturarı bulma
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# konturların içinde gezme
for c in cnts:

	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = detect(c)# hangi şekil olduğunu bulma

	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)# şekillerin kenarlarını çizme 
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)# şeklin ismini yazdırma
     
	cv2.imshow("Image", image)
	cv2.waitKey(0)
