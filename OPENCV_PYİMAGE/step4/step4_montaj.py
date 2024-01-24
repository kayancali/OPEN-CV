

from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=16,
	help="# of images to sample")
args = vars(ap.parse_args())
imagePaths = list(paths.list_images(args["images"]))

random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]
# görseller için liste oluşturduk
images = []

for imagePath in imagePaths:# resimlerin içinde geziyoruz
	
	image = cv2.imread(imagePath)
	images.append(image)# listeye ekliyoruz

montages = build_montages(images, (128, 196), (7, 3))#(128, 196) boyutu - (3, 7) açılan alan boyutu

for montage in montages:
	cv2.imshow("Montage", montage)
	cv2.waitKey(0)