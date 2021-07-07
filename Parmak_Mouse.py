import cv2
import numpy as np
from pynput.mouse import Button, Controller
import tkinter as tk
# Kamera ve maskeleme
cam = cv2.VideoCapture(0) #webcam'i yakalama
# Font
font = cv2.FONT_HERSHEY_SIMPLEX
# Renk araligi secimi
lowerb = np.array([110,80,155])
upperb = np.array([200,120,255])
# Fareyi tanimla
mouse = Controller()
# Arayüz yakalama
root = tk.Tk()
sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()
(camx, camy) = (640, 480)
grainAcik = np.ones((5,5)) # Buna Kernelde denir bosluklari doldurma islemidir
grainKapali = np.ones((20,20))
pinchFlag = 0
while True:
    ret, img = cam.read()
    img = cv2.resize(img,(camx,camy))

    # Hue, Saturation dönümü
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Maskeleme
    mask = cv2.inRange(imgHSV, lowerb, upperb)
    maskeAcik = cv2.morphologyEx(mask, cv2.MORPH_OPEN, grainAcik)  # Morphology yani eritme yöntemi
    maskeKapali = cv2.morphologyEx(maskeAcik, cv2.MORPH_CLOSE, grainKapali)
    maskSecim = maskeKapali
    kontur, h = cv2.findContours(maskSecim.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if(len(kontur)==2):
        #if (pinchFlag == 1):
        #    pinchFlag = 0
        #    mouse.release(Button.left)
        # Parmaklar acik
        x1, y1, w1, h1 = cv2.boundingRect(kontur[0])
        x2, y2, w2, h2 = cv2.boundingRect(kontur[1])
        # Obje Cercevesi olusturma
        cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
        # Objelerin orta noktasi
        cx1 = x1+w1/2
        cy1 = y1+h1/2
        cx2 = x2 + w2 / 2
        cy2 = y2 + h2 / 2
        cx = (cx2+cx1)/2
        cy = (cy1+cy2)/2
        cv2.line(img, (int(cx1), int(cy1)), (int(cx2), int(cy2)), (255, 0, 0), 2)
        cv2.circle(img, (int(cx), int(cy)), 2, (0, 0, 255), 2)
        # Fare tiklama islemleri parmaklar acikken
        '''mouse.release(Button.left)

        mouseLoc = (sx-(cx*sx/camx), cy*sy/camy)
        mouse.position = mouseLoc
        while mouse.position != mouseLoc:
            pass'''

    elif(len(kontur)==1):
        x, y, w, h = cv2.boundingRect(kontur[0])
        #if (pinchFlag == 0):
        #    pinchFlag = 1
        #    mouse.press(Button.left)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cx = x+w/2
        cy = y+h/2
        cv2.circle(img, (int(cx), int(cy)), int((w+h)/4), (0, 0, 255), 2)
        # Fare tiklama islemleri parmaklar kapaliyken
        '''mouse.press(Button.left)

        mouseLoc = (sx-(cx*sx/camx), cy*sy/camy)
        mouse.position = mouseLoc
        while mouse.position != mouseLoc:
            pass'''
    cv2.imshow("Kamera", img)
    cv2.waitKey(5)
