#coding=utf-8

import pyautogui
from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,move_to,log_write,get_mouse_location,adb_test
from setting import *
import time,os,cv2
ocr_load=False

# ocr_extract('./imgs/develop/screenshot18.png')
time.sleep(3)
while True:    
    pyautogui.click(1844,44,button='left')
    time.sleep(0.5)