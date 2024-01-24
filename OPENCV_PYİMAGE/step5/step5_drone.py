#gerekli paketleri ekledik
import cv2
import imutils
import argparse
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() 
ap.add_argument("-v","--video",help="path to the video file")  
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"]) #videomuzu alıyoruz

while True: #frameleri okumak için bir döngü oluşturuyoruz
    ret,frame = cap.read() #frameleri okuyoruz
    status = "No Targets" 

    if ret == 0:  #frameler okunmamışsa döngüden çık
        break

     
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #frameleri gri tonlara çevirdik
    blurred = cv2.GaussianBlur(gray,(7,7),0)  #blur uyguladık
    edged = cv2.Canny(blurred,50,150) #kenarları belirginleştiriyoruz

    cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #konturları buluyoruz
    cnts = imutils.grab_contours(cnts)

    for c in cnts: #konturların içinde geziniyoruz
        
        epsilon = cv2.arcLength(c,True) * 0.01
        approx = cv2.approxPolyDP(c,epsilon,True)

        if len(approx) >= 4 and len(approx) <= 6: #eğer kontur 4 köşeden büyük 6 köşeden küçük ve eşit ise   
            (x,y,w,h) = cv2.boundingRect(approx)     # konturun x,y yani sol üst köşesinin kordinatları yüksekliği ve genişliğini alır   
            aspectRatio = w / float(h)  

            area = cv2.contourArea(c)                   #conturun alanını bulur    
            hullArea = cv2.contourArea(cv2.convexHull(c))  

            solidity = area / float(hullArea)  

            # değerler sağlanıyorsa True değerleri döndürülür
            keepDims = w > 25 and h > 25 
            keepSolidity = solidity > 0.9 # 
            keepAspectRatio  = aspectRatio >= 0.8 and aspectRatio <= 1.2     

            if keepDims and keepSolidity and keepAspectRatio :  # hepsi sağlaıyorsa 
                cv2.findContours(frame,[approx],-1,(0,0,255),4)  #bulunan konturları çiz

                status = "Target(s) Acquired"  

                M = cv2.moments(approx)                                              
                #konturun merkezine '+' işareti ekliyoruz

                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))   
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)

                cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2) 

                cv2.imshow("Frame", frame) #frameler ekrana bastık

                if cv2.waitKey(1) == ord('q'): # çıkış birimi 
                    break

cap.release () #frameleri serbest bırak
cv2.destroyAllWindows()  #tüm pencereleri kapat









