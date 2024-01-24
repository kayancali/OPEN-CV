# gerekli kütüphanelerin eklenmesi
import numpy as np
import argparse
import cv2
# terminal kullanımı için argparse kütüphanesinin kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to BING objectness saliency model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-n", "--max-detections", type=int, default=10,
	help="maximum # of detections to examine")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])# resmin okunması

# resmin en belirgin noktalarının tespit eddilmesi
saliency = cv2.saliency.ObjectnessBING_create()
saliency.setTrainingPath(args["model"])

(success, saliencyMap) = saliency.computeSaliency(image)
numDetections = saliencyMap.shape[0]


# default olarak 10 a kadar bir döngü başlattık
for i in range(0, min(numDetections, args["max_detections"])):

    # bulunan kısımların sınırlayıcı kutu kordinatlarını aldık
	(startX, startY, endX, endY) = saliencyMap[i].flatten()
	
	
	output = image.copy()
	color = np.random.randint(0, 255, size=(3,))# rastgele bir renk için 
	color = [int(c) for c in color]
	# algılanan kısımı dikdörtgen içine aldık
	cv2.rectangle(output, (startX, startY), (endX, endY), color, 2)
	
	cv2.imshow("Image", output)
	cv2.waitKey(0)