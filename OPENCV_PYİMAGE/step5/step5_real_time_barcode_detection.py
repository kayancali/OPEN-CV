#gerekli kütüphaneleri ekledik
from claslar import simple_barcode_detection
from imutils.video import VideoStream
import argparse
import cv2
import time
# terminalden giriş alabilmek için argparse kütüphanesinin kullanımı
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", 
	help="path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video",False):  
    vs = VideoStream(src=0).start() # webcamden görüntü aldık
    time.sleep(1.0)    
else: 
    vs = cv2.VideoCapture(args["video"])


while True:     # framleri okumadk için döngü başlattık
    frame = vs.read()  # framleri okuduk
    frame = cv2.flip(frame,1)# görüntüyü y ekseninde çevirdik 
    frame = frame[1] if args.get("video",False) else frame  

    if frame is None:  # fame yok ise döngüden çık
        break

    # framedeki barkodu tespit etmek için deteck fonksiyonumuzu çağırdık
    box = simple_barcode_detection.detect(frame)  
    if box is not None:       # barkot var ise kutucuk içine aldık
        cv2.drawContours(frame,[box],-1,(0,255,0),2)

    cv2.imshow("frame",frame)    # framleri ekrana bastık
    if cv2.waitKey(1) == ord('q'):      # çıkış birimini ekledik 
        break


if not args.get("video",False):# frame webcamden geldiyse framleri serbes bırakıyoruz
    vs.stop()

else:
    vs.release()  

cv2.destroyAllWindows()  # tüm pencereleri kapat