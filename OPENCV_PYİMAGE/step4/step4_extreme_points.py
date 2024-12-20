import imutils
import cv2
import argparse

# komut argümanları kullanımı
ap =argparse.ArgumentParser()
ap.add_argument("-i","--image",help="image dosyasi yolu")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# resmi gri tonlara çevirdik
gray = cv2.GaussianBlur(gray, (5, 5), 0)# blur uyguluyoruz

# threshold ve morfolojik işlemler
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
# konturları buluyoruz
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)# en büyük konturu buluyoruz
 #en sağ,en sol,en aşağı ve en yukarıdaki konturları döndürüyoruz
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])
# konturu çiziyoruz
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
#en sağ,en sol,en aşağı ve en yukarıdaki kontur koordinatlarına çember çiziyoruz
cv2.circle(image, extLeft, 8, (0, 0, 255), -1) 
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
# resmimizi eranda gösteriyoruz
cv2.imshow("Image", image)
cv2.waitKey(0)