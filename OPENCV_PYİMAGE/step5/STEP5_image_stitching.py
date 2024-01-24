# gerekli kütüphaneleri ekledik
from imutils import paths,is_cv3
import numpy as np
import argparse
import imutils
import cv2
# terminali kullanmak için argarparse kütüphanesinin kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
	help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
ap.add_argument("-c", "--crop", type=int, default=0,
	help="whether to crop out largest rectangular region")
args = vars(ap.parse_args())

print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))# giriş görüntülerini liste halinde okuduk
images = [] # listesini oluşturduk

for imagePath in imagePaths:# giriş görüntülerini images listesine akatardık
	image = cv2.imread(imagePath)
	images.append(image)

print("[INFO] stitching images...")
# görüntüleri birleştirmek için stitcher yapısını oluşturduk
stitcher = cv2.createStitcher() if is_cv3() else cv2.Stitcher_create() 
(status,stitched) = stitcher.stitch(images)


if status == 0:# birleştirme olmuş ise 
    print("islem basarili")
    #  birleştirimiş görüntüyü çevreleyen 10 piksellik bir çerçeve oluşturduk
    stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,cv2.BORDER_CONSTANT, (0, 0, 0))

    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)# gri formata çevirdik
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]# threshold uyguladık

# konturları bulduk
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)# en büyük konturu c ye atadık

mask = np.zeros(thresh.shape, dtype="uint8")# mask uyguladık
(x, y, w, h) = cv2.boundingRect(c)# c nin sol üst küşesinin konumu yüksekliği ve gemişliğini aldık
cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)# bir diktörtgen çizdik

# mask ın iki kopyasınnı oluşturduk 
minRect = mask.copy()
sub = mask.copy()

while cv2.countNonZero(sub) > 0:# sıfırdan farklı piksel kalmayıncaya kadar kadar devam et
    
    minRect = cv2.erode(minRect, None)# morfolojik işlem uyguladık
    sub = cv2.subtract(minRect, thresh)
	
    # kontur işlemlerini tekarladık
    cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(c)
    
    stitched = stitched[y:y + h, x:x + w]# sınırlayıcı dikdörtgeni tam ekran yaptık
    # çıktı görüntüsünü kaydettik
    
    cv2.imshow("Stitched", stitched)# çıktıyı ekrana bastık
    cv2.waitKey(0)
   
else:# işlem gerçekleşmez ise hata mesajı verir
    print("[INFO] image stitching failed ({})".format(status))