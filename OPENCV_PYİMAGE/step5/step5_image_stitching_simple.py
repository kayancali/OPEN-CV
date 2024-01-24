#gerekli kütüphanelerin eklenmesi
from imutils import paths, is_cv3
import cv2
import argparse
import numpy as np       
# terminalden kontrol için argaparse kütüphanesi kullandık
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--images",type=str,required=True, 
    help ="path to input directory of images to stitch")
ap.add_argument("-o","--output",type=str,required=True,
    help="Path to the output image")
args = vars(ap.parse_args())

imagePaths = sorted(list(paths.list_images(args["images"]))) #terminalden aldığımız görüntüleri liste halinde sıralıyoruz
images = [] #images isminde bir liste oluşturuyoruz

for imagePath in imagePaths: #resimlerin içinde geziniyoruz
    image = cv2.imread(imagePath) 
    images.append(image) #teker teker resimleri images listesine ekliyoruz

stitcher = cv2.createStitcher() if is_cv3() else cv2.Stitcher_create()  # panorama oluşturucu nesnesi oluştururuz
(status,stitched) = stitcher.stitch(images) #listedeki görüntüleri birleştiriyoruz

if status == 0: #eğer birleştirme işlemi başarılı ise 
    cv2.imwrite(args["output"],stitched) #çıkış görüntüsünü kaydederiz
    cv2.imshow("stitched",stitched) #panorama görüntüsünü imshowluyoruz
    cv2.waitKey(0) 

else:  #başarılı değilse hata mesajı gönderir
    print("failed ({})".format(status))
