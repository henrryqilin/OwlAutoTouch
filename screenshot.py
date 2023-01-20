import os
from basic import adb_test,get_screen

log_list = os.listdir(path='./imgs/develop')#整理logs文件夹中的日志文件
number = len(log_list)

adb_test()
get_screen(save_location = f'./imgs/develop/screenshot{number}.png')