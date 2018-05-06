#encoding: utf-8
from PIL import ImageGrab
import cv2;
import aircv;
import win32api;
import win32con;
import time, os,sys;
import numpy;
#截图
def screen():
    img = ImageGrab.grab(bbox=(0, 0, 600,900));
    #img.save("d://ttt.png")
    return img

#寻找红包
def findrb(pic):
    pic = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)
    #pic = cv2.imread("d://ttt.png")
    rb = cv2.imread("d://rb.png")
    pos = aircv.find_template(pic,rb,0.99)
    if (pos==None):
        sys.exit()
    circle_center_pos = pos['result']
    target = (int (circle_center_pos[0]),int(circle_center_pos[1]))
    return target
#模拟点击
def winop(target):
    win32api.SetCursorPos([target[0], target[1]])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(1)
    #固定位置打开红包
    win32api.SetCursorPos([210,420])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(1)
    #退出
    win32api.SetCursorPos([20,65])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print('恭喜你抢到一个红包')
#颜色判断防止点击点过的红包
def realcolor(target,pic):
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
    point = pic[target[0], target[1]]
    print point[1]
    if (point[1]>=46):
        return False
    else:
        return True
if __name__ == '__main__':
    img = screen()
    target = findrb(img)
    winop(target)