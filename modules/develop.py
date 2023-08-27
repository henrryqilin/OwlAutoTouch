#coding=utf-8

ocr_load=True

import pyautogui
from basic import get_screen,click_change,move_to,log_write,get_mouse_location,adb_test,img_recognition,ocr_recognition
from setting import *
import time,os,cv2

a=ocr_recognition()
a.result('./imgs/develop/p1.png')
print(a.find('月女的华彩'))

# b=img_recognition()
# b.get_xy(['close','bag','five_star'])
# if b['close'][0] == True:
#     move_to(b['close'][1])
#     click_change(b['close'][1])
