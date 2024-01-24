import argparse
import imutils
import cv2
# komut satırı kullanmak için 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars ( ap. parse_args ())

image = cv2.imread(args["image"])# resimi komut satırından okuma

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# resmi gri tona çevirdik

kenar= cv2.Canny(gray,30,150)# nesnelerin kenarlarını algılama 30 min değer 150 max değer 

thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]

# cv2.imshow("Image", kenar)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # şekillerin kontürlerini bulduk
cnts = imutils.grab_contours(cnts)
output = image.copy()

for c in cnts:# tüm kontürleri gezdik

	cv2.drawContours(output, [c], -1, (240, 0, 159), 3) # kontürleri sırayla çizdik
text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,(240, 0, 159), 2)# resme yazı yazdık

mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)# resimdekii şekilleri küçültüyor
cv2.imshow("Eroded", mask)

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)# resimdeki şekilleri büyütüyor
cv2.imshow("Dilated", mask)

mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)# bitwise kullnarak yalnızca şekilleri gösterdik

cv2.imshow("output", output)
cv2.waitKey(0)