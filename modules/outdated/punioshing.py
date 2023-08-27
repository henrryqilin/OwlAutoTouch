#coding=utf-8

import time
from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,log_write,adb_test
from setting import *

if adb_test() :
    print('连接成功')
else :
    connect_mode = 0
    print('adb连接失败,请检查地址设置,以及是否安装ADB')

def start_up() :
    '''
        启动战双，暂不支持打开软件
    '''
    get_screen()
    if '战双帕弥什' in ocr_extract() :#登录界面
        pass
    elif '游戏初始化' in ocr_extract() :
        pass
    elif '成员' in ocr_extract() and '任务' in ocr_extract() and '研发' in ocr_extract() :#主界面
        pass
    elif get_xy('./imgs/models/return.png',mode = 1)[0] :
        pass
    elif get_xy('./imgs/models/home.png',mode = 1)[0] :
        pass