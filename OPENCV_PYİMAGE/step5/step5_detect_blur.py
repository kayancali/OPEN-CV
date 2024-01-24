# gerekli kütüphaneleri ekledik
from imutils import paths
import argparse
import cv2


# laplacian komutu kenarların ne kadar belirgin olduğunu ölçer
def variance_of_laplacian(image): 
    # var fonksiyonu varyans hesaplar 
    return cv2.Laplacian(image,cv2.CV_64F).var() 

# terminali kullanmak için argparse kütüphanesnin kullanımı
ap = argparse.ArgumentParser()  
ap.add_argument("-i", "--images", required=True, 
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# giriş görüntülerini liste şeklinde tek tek geziyoruz
for imagePath in paths.list_images(args["images"]): 
    image = cv2.imread(imagePath)  # giriş görüntülerini sırasıyla image değişkenşne atadık 
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  # gri formata çevirdik
    fm = variance_of_laplacian(gray)      # bulunan varyans fm değişkenine atadık
    text = "Bulankk degil" 
    
    # threshold değerini defould olarak 100 atamıştık 100 den küçük ise bulanık
    if fm < args["threshold"]:    
        text = "Bulanik"
 #bulunan sonuçları görüntü üzerine yazdık
    cv2.putText(image,"{}: {:.2f}".format(text,fm),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),3) 
    cv2.imshow("Image",image)
    if cv2.waitKey(0) == ord('q'):     
        break
