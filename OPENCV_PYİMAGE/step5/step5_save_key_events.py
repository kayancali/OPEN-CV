from KeyClipWriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
# terminali kullanmak için argparse kütüphanesini kullanıyoruz
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-b", "--buffer-size", type=int, default=32,
	help="buffer size of video clip writer")
args = vars(ap.parse_args())


vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

kcw = KeyClipWriter(bufSize=args["buffer_size"])# video kayıtları için kullandığımız fonksiyonların classı
consecFrames = 0

while True:
      
        frame = vs.read()# frameleri okuyoruz
        frame = imutils.resize(frame, width=600)# yeniden boyutlandırıyoruz
        updateConsecFrames = True
        
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)# blur ekliyoruz
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)# hsv formatına çeviriyoruz

        mask = cv2.inRange(hsv, greenLower, greenUpper)# mask uyguluyoruz
        # morfolojik işlemler uyguluyoruz 
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # konturları buluyoruz
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # kontur varsa 
        if len(cnts) > 0:
           
            c = max(cnts, key=cv2.contourArea)# alanı en büyük kontururu buluyoruz
            ((x, y), radius) = cv2.minEnclosingCircle(c)# minimum çemberin merkez noktalarının koordinatlarını ve yarıçapı değerini döndürür.
            updateConsecFrames = radius <= 10
            
            if radius > 10:# yarıçap 10 dan büyükse  
              
                consecFrames = 0
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)# çember içine aldık
  
                if not kcw.recording:# kayıt yapılmıyorsa 
                        timestamp = datetime.datetime.now()# anlık zaman
                        p = "{}/{}.avi".format(args["output"],# kaydedeceğimiz yolu belirler
                            timestamp.strftime("%Y%m%d-%H%M%S"))
                        kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),args["fps"])#videoyu kaydetmeye başlıyoruz p dosyanın yolu, karekter kodu ve kare hızını parametre olarak alırız
                        
                if updateConsecFrames:
                    consecFrames += 1
                
                kcw.update(frame)
                
                if kcw.recording and consecFrames == args["buffer_size"]:
                    kcw.finish()
                
                cv2.imshow("Frame", frame)# frame leri gösterdik
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord("q"):
                    break

if kcw.recording:#eğer hala kayıt yapılıyorsa kaydı durdururuz
    kcw.finish()

cv2.destroyAllWindows()
vs.stop()#web camden alınan görüntüyü durdururuz