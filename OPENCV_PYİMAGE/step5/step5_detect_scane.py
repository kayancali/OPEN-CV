# gerekli kütüphanelerin eklenmesi
import argparse
import imutils
import cv2
import os

# terminalin kullanılması için argparse kütüphanesinin kullanılması
ap = argparse.ArgumentParser()       
ap.add_argument("-v", "--video", required=True, type=str,     
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str,
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0, 
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=10.0,
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=200,
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())

# arka plan çıkarıcı komutumuzu fgbg değişkenşne atadık
fgbg = cv2.createBackgroundSubtractorMOG2() 

# kullanılacak değişkenleri tanımladık
captured = False   
total = 0
frames = 0

# terminalden çekilen videoyu aldik
vs = cv2.VideoCapture(args["video"])  
W, H = (None, None)   
while True:     # framleri pokumak içiin döngü başlattık
    ret,frame = vs.read()    

    if frame is None:        # frame yok ise döngüden çık
        break     

    orig = frame.copy()  
    frame = imutils.resize(frame,width=400)   # framleri yeniden boyutlandırdık
    mask = fgbg.apply(frame)# arka plan çıkarıcıyı uyguladık
    
    # gerekli morfolojik işlemleri uyguladık
    mask = cv2.erode(mask, None, iterations=2)  
    mask = cv2.dilate(mask, None, iterations=2) 


    if W is None or H is None:  # genişlik ve yükseklik none ise 
        H, W = mask.shape[:2]   # framlerin boyutunu yakala

    p = (cv2.countNonZero(mask) / float(W * H)) * 100# maskenin yüzdesini hesapladık


# framlerdeki ön plan maskenin yüzdesinden az ise 
    if p < args["min_percent"] and not captured and frames > args["warmup"]:   

        captured = True  # yakalanan frame 


        fileName = " {}.png".format(total)  
        path = os.path.sep.join([args["output"],fileName]) 
        total +=1 

        print("kaydediliyor {}".format(path))
        cv2.imwrite(path,orig)# orjinali ve yükek çözünürlüklüyü kaydettik
    elif captured and p>= args["max_percent"]:  # ilk if sağlanıyorsa ve p değeri arka plandan büyükse  
        captured = False
    # imshowlarımız
    cv2.imshow("Frame", frame) 
    cv2.imshow("Mask", mask) 
    if cv2.waitKey(1) == ord('q'):  # çıkış birimini ekledik
        break

    frames +=1 

vs.release()  