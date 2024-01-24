#gerekli kütüphanleri ve paketleri çağırma
from sqlite3 import Timestamp
from imutils.video import VideoStream
from claslar.basicmotiondetector import BasicMotionDetector
from claslar.panorama import Stitcher

import numpy as np
import imutils
import time
import cv2
import datetime

leftStream = VideoStream(src=0).start()   #webcamdan görüntü aldık
rightStream = VideoStream(usePiCamera=True).start()# Raspberry Pi kameradan görüntü alır  
time.sleep(1.0) #sistemi 1 saniyelik bir gecikme ile başlatırız

stitcher = Stitcher() # görüntü bu fonksiyon ile birleştirilir
motion = BasicMotionDetector(minArea= 500)  
total = 0

while True:  
    leftFrame = leftStream.read()  #webcamden ve Raspberry Pi kameradan frameleri okuruz
    rightFrame = rightStream.read()

    leftFrame = imutils.resize(leftFrame,width=400)#framelerimizi yeniden boyutlandırdık
    rightFrame = imutils.resize(rightFrame,width=400) #genişlik  400 

# 2 farklı görüntü burada panaromik olarak birleştirilir
    result = stitcher.stitch([leftFrame,rightFrame])  
     

    if result is None:  #sonuç none ise 
        print("homografi hesaplanamadi")
        break #döngüden çık

    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)  # resmi  gray formata çeviririz
    gray = cv2.GaussianBlur(gray,(21,21),0)  #blur uygularız
    locs = motion.upadate(gray)# İşlenen panorama daha sonra hareket detektörüne geçirilir.
    
    if total > 32 and len(locs) > 0:
        (minX,minY) = (np.inf,np.inf)
        (maxX,maxY) = (-np.inf,-np.inf)

        for l in locs:
            (x,y,w,h) = cv2.boundingRect(l)
            (minX,minY) = (min(minX,x),max(maxX ,x + w))
            (minY, maxY) = (min(minY, y), max(maxY, y + h))

        cv2.rectangle(result,(minX,minY),(maxX,maxY),(0,0,255),3)

    total +=1
    timestamp = datetime.datetime.now()    #anlık zamanı döndürür         
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")    
    cv2.putText(result, ts, (10, result.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Result", result)  #birleştirilmiş görünüyü imshowlarız
    cv2.imshow("Left Frame", leftFrame)  
    cv2.imshow("Right Frame", rightFrame) 
    
    if cv2.waitKey(1) == ord('q'): # çıkış birimi
        break


cv2.destroyAllWindows() #tüm pencereleri kapat 
leftStream.stop() #webcamden görüntü almayı durdur
rightStream.stop() #Raspberry Pi kameradan görüntü almayı durdur






