import os,time
from basic import adb_test,get_screen


adb_test()

def screenshot(mode=0,sleep=3,name=''):
    """
    mode:int类型,0为截图命名为时间,1为截图命名为screenshot+数字
    sleep:int类型,
    name:str类型,保存的文件名,如果存在且不为空字符串则以该参数命名截图
    return:None
    """
    if mode == 0 and name == '':   
        time_now = time.strftime("%Y-%m-%d %H.%M.%S",time.localtime())
        get_screen(save_location = f'./imgs/develop/{time_now}.png')
    
    elif mode == 1 and name != '':
        img_list = os.listdir(path='./imgs/develop')
        copy_list=img_list.copy()
       
        for i in img_list:
            if 'screenshot' in i:
                copy_list.remove(i)
        number = len(img_list)-len(copy_list)
        get_screen(save_location = f'./imgs/develop/screenshot{number}.png')
    
    elif name != '':
        get_screen(save_location = f'./imgs/develop/{name}.png')
    time.sleep(sleep)
    return

while True:
    screenshot(1)
    print('完成！')