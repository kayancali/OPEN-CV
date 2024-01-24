#gerekli kütüphaneleri ekledik
import cv2
import numpy as np
import argparse
import imutils
# terminalden terminaeli kullanabilmek için argparse kütüphanesini kullandık
ap = argparse.ArgumentParser() 
ap.add_argument("-i", "--image", required = True, 
	help = "path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  #görüntüyü okuduk
image = imutils.resize(image,width=500) #yeniden boyutandırdık
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #gri tonlara çevirdik

#gradyan büyüklüğü temsilini oluşturmak için Scharr operatörünü kullandık
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F  
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)  
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY) # y gradyanını x gradyanından çıkarttık
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient, (9, 9))        # blur uyguladık
ret,thresh = cv2.threshold(blurred,225,255,cv2.THRESH_BINARY) # threshold uyguladık

# bu komut barkodun dikey şeritleri arasındaki boşlukları kapattık
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))   
# görüntüyü netleştirmek için morfolojik işlem uyguladık   
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  
    
closed = cv2.erode(closed, None, iterations = 4)   

closed = cv2.dilate(closed, None, iterations = 4)  

# konturları bulduk
cnts = cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
cnts = imutils.grab_contours(cnts)

# en büyük konturu c ye atadık
c = sorted(cnts,key=cv2.contourArea,reverse=True)[0]   

rect = cv2.minAreaRect(c) #en büyük kontur için minimum sınırlayıcı kutuyu belirledik ve bir dikdörtgen oluşturduk
box = cv2.boxPoints(rect) if imutils.is_cv2 else cv2.boxPoints(rect)   #dikdörtgenin köşe noktalarını aldık
box = np.int0(box)         # ondalıklı koordinatları tam sayıysa döndürür.
# blirlediğimiz kutucuğu çizdik
cv2.drawContours(image,[box],-1,(0,255,0),3)

cv2.imshow("image",image)  #çıktımızı görüntüleriz  

cv2.waitKey(0)
