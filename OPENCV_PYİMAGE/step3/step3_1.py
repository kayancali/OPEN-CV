import imutils
import cv2

image = cv2.imread("pyimage.jpg") # resim okuma
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d)) # resim boyutlarını gösterme

( B, G, R ) = image [ 100 , 50 ] #  100,50 konumundaki pixelin b g r değerlierini öğrenme
print ( "R={}, G={}, B={}" .format ( R, G, B ))

resized = cv2.resize(image, (200, 200)) # resmi yeniden boyutlandırma 
#cv2.imshow("Fixed Resizing", resized)

roi = image[60:160, 150:420] # resimden konumları verilen bi bölümü ayırma
#cv2.imshow("ROI", roi)

# resmin en boy oranını bozmadan yeniden boyutlandırma
r = 300.0 / w
dim = (300, int(h * r))
resized = cv2.resize(image, dim)
# cv2.imshow("Aspect Ratio Resize", resized)


# en boy oranını bozmadan imutils kütüphanesi ile resmi yeniden boyutlandırma
resized = imutils.resize(image, width=300)
# cv2.imshow("Imutils Resize", resized)


# resmi döndürme 
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
# cv2.imshow("OpenCV Rotation", rotated)

# döndürme işlemini imutils yardımı ile oluşturma 
rotated = imutils. rotate ( image, -45 )
# cv2. imshow ( "Imutils Döndürme" , rotated )

# resmi kırpmadan döndürmek için bu komutu kullanırız
rotated = imutils.rotate_bound(image, 45)
# cv2. imshow ( "Imutils Döndürme" , rotated )

blurred = cv2.GaussianBlur(image, (11, 11), 0)# resmi blurlama 
 # cv2.imshow("Blurred", blurred)

# resme dikdörtgen çizme 
output = image.copy()
cv2.rectangle(output, (320, 60), (420, 180), (0, 0, 255), 2)
#cv2.imshow("Rectangle", output)

# resme daire çizme 
output = image.copy()
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
# cv2.imshow("Circle", output)

# resme çizgi çizme 
output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
# cv2.imshow("Line", output)

# resme yazı yazma 
output = image.copy() 
cv2.putText(output, "selamun aleykum", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
# cv2.imshow("Text", output)


cv2.waitKey(0)




