# gerklii kütüphaneleri ekledik
from skimage import transform
from skimage import filters
import argparse
import cv2

# terminal kullanımmı için argparsse kütüphanesinin kullanımı
ap = argparse.ArgumentParser()         
ap.add_argument("-i", "--image", required=True,  
	help="path to input image file")
ap.add_argument("-d", "--direction", type=str,
	default="vertical", help="seam removal direction")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # remsi okuduk
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grii tonlara çevirdik

# sobel filtesini uyguladık
mag = filters.sobel(gray.astype("float"))
cv2.imshow("ORIGINAL",image) # orjinal resmi ekrana bastık

for numSeams in range(20,140,20): # birkaç sayıyı kullanarak dikiş işlemini gerçekleştirdik
    
    carved =transform.seam_carve(image,mag,args["direction"],numSeams) 

    print("[INFO] removing {} seams; new size: ""w = {} ,h = {}".format(numSeams,carved.shape[1],carved.shape[0])) 
    
    cv2.imshow("carved",carved) 
    cv2.waitKey(0) 

    