import os,time
from basic import adb_test,get_screen


# adb_test()

while True :
    log_list = os.listdir(path='./imgs/develop')
    number = len(log_list)
    time_now = time.strftime("%Y-%m-%d %H.%M.%S",time.localtime())
    get_screen(save_location = f'./imgs/develop/{time_now}.png')
    time.sleep(3)