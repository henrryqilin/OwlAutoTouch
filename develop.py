#coding=utf-8

ocr_load=True

import pyautogui
from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,move_to,log_write,get_mouse_location,adb_test,img_recognition,ocr_recognition
from setting import *
import time,os,cv2

a=ocr_recognition()#chenyulin
a.result('./imgs/develop/2023-03-05 20.31.20.png')
print(a.find('月女的华彩'))