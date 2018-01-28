#encoding: utf-8
import cv2
import numpy as np

facepic = cv2.imread("d://face222.jpg")
hatpic = cv2.imread("d://hat2.png")

hsv = cv2.cvtColor(hatpic,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,np.array([12,216,255]),np.array([12,216,255]))
cv2.imshow("test3", mask)
def makehat(x,y,w,h,src,target,mask):
    #原图按比例缩小
    tHeight = target.shape[0]
    tWidth = target.shape[1]
    target = cv2.resize(target,(w,int (w*tHeight/tWidth)),0,0,cv2.INTER_AREA)
    # 掩膜按比例缩小
    mask = cv2.resize(mask, (w, int(w * tHeight / tWidth)), 0, 0, cv2.INTER_AREA)

    for i in range(target.shape[0]):
        for j in range(target.shape[1]):
            if mask[i,j]==0:
                src[y-int(h/1.3)+i,x+j] = target[i,j]

    #src[y:int (y+w*tHeight/tWidth),x:x+w] = target


faceCasacade = cv2.CascadeClassifier('C:/Users\Leo.guo\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml');
gray = cv2.cvtColor(facepic,cv2.COLOR_BGR2GRAY)
faces = faceCasacade.detectMultiScale(gray);

for (x,y,w,h) in faces:
    if (w>50 and h>50):
        cv2.rectangle(facepic, (x, y), (x + w, y + h), (0,0,255), 1)
        #makehat(x,y,w,h,facepic,hatpic,mask)
cv2.imwrite('d://abc.jpg',facepic)
cv2.imshow("test", facepic)
cv2.waitKey()


