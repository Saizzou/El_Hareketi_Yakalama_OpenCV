import cv2
import numpy as np
import sys

image_hsv = None   
pixel = (20,60,80) 
(camx, camy) = (640, 480)

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #Üst ve Alt HSV degeri burda oynamalar yapabilirsiniz(+-10):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)

        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)

def main():
    global image_hsv, pixel 

    cam = cv2.VideoCapture(0)
    ret, img = cam.read()
    img = cv2.resize(img, (camx, camy))
    cv2.imshow("bgr",img)

    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    image_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",image_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
