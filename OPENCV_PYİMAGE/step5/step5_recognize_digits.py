from imutils.perspective import four_point_transform   
from imutils import contours 
import imutils
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
args = vars(ap.parse_args()) 

# rakam bölümlerinin sözlüğü ve keyleri
DIGITS_LOOKUP = {           
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

image = cv2.imread(args["images"]) #resmi okuruz
image = imutils.resize(image,height=500)  #resmi yeniden boyutlandırdık
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #resmi gri tona çevirdik
blurred = cv2.GaussianBlur(gray,(5,5),0)   #blur uyguladık
edged = cv2.Canny(blurred,50,200,255)

 # konturları bulduk
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)  #bulduğumuz konturları büyükten küçüğe sıraladık
displayCnt = None 

# köşe sayısını bulmak için for döngü ve işlemeler
for c in cnts:
    epsilon = cv2.arcLength(c,True) * 0.02        
    approx = cv2.approxPolyDP(c,epsilon,True)
 #for ile içinde gezindiğimiz en büyük konturun köşe sayısı dört ise
    if len(approx) == 4:           
        displayCnt = approx        
        break

#perspektif dönüşümü uyguladık kuş bakışı görüntü elde ettik
warped = four_point_transform(gray,displayCnt.reshape(4,2))     
output =  four_point_transform(image,displayCnt.reshape(4,2)) 

 # çarpık görüntünün eşiğini belirledik  ardından bir dizi morfolojik işlem uyguladık
ret,thresh = cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,5))   
thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)

#temizlediğimiz görüntünün konturlarını bulduk
cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
cnts = imutils.grab_contours(cnts)
digitCnts= []



for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)#konturun koordinatlarını bulduk
    
    if w >= 15 and (h >= 30 and h <= 40): # genişlik ve yüksekli istenildiği gibi ise
        digitCnts.append(c)               #  konturu digitCnt listesine ekledik

digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0] # digitCnt içindeki conturları soldan sağa sıraladık
digits = []

for c in digitCnts:                     #rakam konturlarındaa döngü başlattık
    (x,y,w,h) = cv2.boundingRect(c)       
    roi = thresh[y:y+h,x:x+w]       #thresh görüntüsünden ilgileneceğimiz alanı roi değişkenine attık

    #rakamların her biri için sınırlayıcı bir kutu oluşturuyorduk
    (roiH,roiW) = roi.shape            #roi görüntülerinin genişlik ve yüksekliğini hesaplıyoruz
    (dW,dH) = (int(roiW * 0.25),int(roiH * 0.15))    #ROI boyutlarına dayalı olarak her segmentin yaklaşık genişliğini ve yüksekliğini hesaplıyoruz.
    dHC = int(roiH * 0.05)  

    # segmentlerin x ve y koordinatlarının bir listesini tanımladık
    segments = [    
		((0, 0), (w, dH)),	# en üst
		((0, 0), (dW, h // 2)),	# üst-sol
		((w - dW, 0), (w, h // 2)),	# üst-sağ
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # orta
		((0, h // 2), (dW, h)),	# alt-sol
		((w - dW, h // 2), (w, h)),	# alt-sağ
		((0, h - dH), (w, h))	# en alt
	]
    on = [0] * len(segments)     # 7 tane 0'lardan oluşan bir dizi oluşturup on değişkenine atıyoruz.                          

    for (i,((xA,yA),(xB,yB))) in enumerate(segments):   # 7 tane olan her parçanın üzerinde döngü yapıyoruz
        segROI = roi[yA:yB,xA:xB]           #her parçanın roisini çıkarıyoruz
        total = cv2.countNonZero(segROI)    # sıfır olmayan piksel sayısını total değişkenine atıyoruz.
        area = (xB-xA) * (yB-yA)         
        
        if total / float(area) > 0.5:  #Sıfır olmayan piksellerin toplam alana oranı %50 den büyükse segmentin açık olduğunu düşünebiliriz
            on[i] = 1
    # keyError hatasına karşın try except bloları oluşturduk
    try:                           
        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)
        cv2.rectangle(output,(x,y),(x + w,y + h),(0,255,0),1)
        cv2.putText(output,str(digit),(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,0),2)
    except KeyError: 
        continue

cv2.imshow("image",image)
cv2.imshow("output",output)

cv2.waitKey(0)
cv2.destroyAllWindows()