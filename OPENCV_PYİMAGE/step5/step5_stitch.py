
# gerekli kütüphaneler ve görüntü birleştirme kodu çağrılması
from claslar.panorama import Stitcher
import argparse
import imutils
import cv2
# komut satırı argümanları
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
	help="path to the first image")
ap.add_argument("-s", "--second", required=True,
	help="path to the second image")
args = vars(ap.parse_args())
# birleştirilecek olan görüntüleri okuma
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])
# iki görüntüyüde aynı boyuta getirme 
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)
# stitch kodları ile panaroma işlemini yapma
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
# show the images
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)
cv2.waitKey(0)