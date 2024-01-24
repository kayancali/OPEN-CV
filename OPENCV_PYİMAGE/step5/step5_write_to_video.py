from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
# terminal kullanımı için argaparse kütüphanesinin kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

while True:

        frame = vs.read()# frame lerin okunması
        frame = imutils.resize(frame, width=300)# yeniden boyutlandırma

        if writer is None:# yazılma başlamadıysa

            (h, w) = frame.shape[:2]# frame boyutlarını aldık
            writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
                (w * 2, h * 2), True)# ilk parametre çıkti videosunun yolu ikinci bilmiyom üçüncü istenen fps daha sonra genişlik ve yükseklik 
            zeros = np.zeros((h, w), dtype="uint8")

        (B, G, R) = cv2.split(frame)# framleri rgb bileşenlerine ayırdık
        R = cv2.merge([zeros, zeros, R])
        G = cv2.merge([zeros, G, zeros])
        B = cv2.merge([B, zeros, zeros])
        
        # çıkış çerçevesini oluşturuyoruz
        output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
        output[0:h, 0:w] = frame # orjinal frame 
        output[0:h, w:w * 2] = R # sağ üstte kırmızı framler
        output[h:h * 2, w:w * 2] = G # sağ altta yeşil frameler 
        output[h:h * 2, 0:w] = B # sol altta mavi frameler
        
        writer.write(output)# çıktıyı dosyaya yazdırdık
        cv2.imshow("Frame", frame)# orjinal frame 
        cv2.imshow("Output", output)# çıkış çerçevesi imshow
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break

cv2.destroyAllWindows()
vs.stop()
writer.release()