# gerekli kütüphanleri ekledik
from imutils.video import VideoStream
import imutils
import time
import cv2

saliency = None
vs = VideoStream(src=0).start()# webcamı başlattık
time.sleep(2.0)# 2 saniye bekle

while True:# webcamden dramleri okumak için döngü açtık
       
        frame = vs.read()# framleri okuduk
        frame = cv2.flip(frame,1)# frameleri y ekseiinine göre çevirdik
        frame = imutils.resize(frame, width=500)# yeniden boyutlandırdık
        
        if saliency is None:# değer none ise 
            # en eblirgin noktaları bulduk
            saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()
            saliency.setImagesize(frame.shape[1], frame.shape[0])
            saliency.init()
            

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# gri tonlara çevirdik
        
        (success, saliencyMap) = saliency.computeSaliency(gray)
        # değerleri 0, 250 arasında aldık
        saliencyMap = (saliencyMap * 255).astype("uint8")
       
        cv2.imshow("Frame", frame)
        cv2.imshow("Map", saliencyMap)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):# çıkış birimi
            break
    
cv2.destroyAllWindows()
vs.stop()