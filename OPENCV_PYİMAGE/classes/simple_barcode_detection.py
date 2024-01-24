#gerekli kütüphaneleri ekledik
import numpy as np 
import cv2
import imutils

def detect(image):
    # resmi gri tonlara çevirdik
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    #gradyan büyüklüğü temsilini oluşturmak için Scharr operatörünü kullandık 
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F   
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # gradyan y den x i çıkardık
    gradient = cv2.subtract(gradX, gradY)    
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))# blur uyguladık  
    # threshold binary uygulayarak görüntüdeki siyahları diğer renklerden ayrıdık  
    ret,thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY) 
    # barkoddaki dikey çizgilerin arasını doldurduk ve çeşitli morfolojik işlemler ile net bir kontur elde ettik
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7)) 
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) 
    closed = cv2.erode(closed, None, iterations=4) 
    closed = cv2.dilate(closed, None, iterations=4)

    # kontur bulduk
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) == 0: # kontur bulamaz ise 
        return None # birşey döndürdme
    
    # en büyük konturu c ye atadık ve çevresine bir dikdörtgen çizdik
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0] 
    rect = cv2.minAreaRect(c) 
    box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect) #döndürülmüş dikdörtgenin köşe noktalarını döndürür.
    box = np.int0(box)    
 
    return box # bulunan barkodu döndürdük
