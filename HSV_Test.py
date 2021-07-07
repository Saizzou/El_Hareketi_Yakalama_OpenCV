import cv2
import numpy as np
# Kamera ve maskeleme
cam = cv2.VideoCapture(0) #webcam'i yakalama
# Font
font = cv2.FONT_HERSHEY_SIMPLEX
# Renk araligi secimi
lowerb = np.array([110,80,155])
upperb = np.array([200,120,255])
while True:
    ret, img = cam.read()  # ret: kamera varligini kontrol eder
    img = cv2.resize(img, (240,220)) #boyutlandirma
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Hue-Saturation-Value formatina döndürme
    # Maske ve Grain ayari
    mask = cv2.inRange(imgHSV, lowerb, upperb) # Renk araligini tarama (beyaz gösterir kalani siyah)
    grainAcik = np.ones((5,5)) # Buna Kernelde denir bosluklari doldurma islemidir
    grainKapali = np.ones((20,20)) # büyük doldurma icin kullanim
    maskeAcik = cv2.morphologyEx(mask, cv2.MORPH_OPEN, grainAcik) #Morphology yani eritme yöntemi
    maskeKapali = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, grainKapali)
    """Burda taramak istedigimiz alan hangisi ile daha yakin olursa
    o maske alanini seceriz yada maske alanlarinda degisiklik yapabiliriz
    """
    maskSecim = maskeKapali
    # Kontur ayarlayip cizelim
    kontur, h = cv2.findContours(maskSecim.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, kontur, -1, (255,0,0),3)

    for i in range(len(kontur)):
        x,y,w,h = cv2.boundingRect(kontur[i])
        cv2.rectangle(img, (x,y),(x+w, y+h), (0,0,255),2)
        cv2.putText(img,str(i+1), (x,y+h),font,1,(0,255,255))

    cv2.imshow("Cam", img)
    cv2.imshow("Renk Tarama", mask)
    cv2.imshow("maskeAcik", maskeAcik)
    cv2.imshow("maskeKapali", maskeKapali)
    cv2.waitKey(10)
