#coding=utf-8

import time
from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,log_write,adb_test
from setting import *

if adb_test() :
    print('连接成功')
else :
    print('adb连接失败,可能是端口设置原因')
