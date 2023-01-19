#coding=utf-8

from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,move_to,log_write,get_mouse_location,adb_test
from setting import *
import time,os

adb_test()
get_screen(save_location = './imgs/develop/screenshot1.png')