#coding=utf-8

if __name__ == '__main__' :
    print('这是basic程序,不是启动程序')

import cv2,pyautogui,time,os
from paddleocr import PaddleOCR, draw_ocr
from setting import *

def log_organize():
    log_list = os.listdir(path='./logs')#整理logs文件夹中的日志文件
    log_list.sort(reverse = True)
    # print(log_list)

    if len(log_list) > logs_quantity :

        for i in log_list[logs_quantity:len(log_list)] :
            os.remove(f'./logs/{i}')

    log_time = time.strftime("%Y-%m-%d %H.%M.%S",time.localtime())#创建本次运行日志文件
    log = open(f'./logs/{log_time}.txt','w',encoding = 'utf-8')
    log.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+' 开始运行\n')
    log.close()
    del log
    return log_time

log_name=log_organize()

def log_write(str = '',aim = f'./logs/{log_name}.txt',mode = 'a',code = 'utf-8') :
    """
        将指定的字符按指定的模式写入指定文件
        aim:str类型,文件名或'./logs/log.txt'
        mode:str类型,    'w'以写入的方式打开文件,会覆盖已存在的文件
                        'a'以写入模式打开,如果文件存在,则在末尾追加写入
        str:str类型,写入的内容
        code:str类型,文件打开格式
        return:none
    """
    log = open(aim,mode,encoding = code)
    log.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+' '+str+'\n')
    log.close()
    return#log_write

def get_screen(shot_change = None,mode = connect_mode,save_location = './imgs/screenshot.png',aim = connect_aim)    :
    """
        截取屏幕
        shot_change:tuple类型,偏移的坐标,(x坐标,y坐标,x轴长度,y轴长度)
        save_location:str类型,截图保存的地址
        return:None
    """
    if mode == 0 :
        pyautogui.screenshot(region = shot_change).save(save_location)
    else :
        name = save_location[save_location.find('screen'):len(save_location)]
        path = save_location[0:save_location.find('screen') - 1]
        os.system(f'adb -s {aim} shell screencap -p /sdcard/{name}')
        os.system(f'adb -s {aim} pull sdcard/{name} {path}')

    return#get_screen

def click_change(clickpoint,changex = 0,changey = 0,mode = connect_mode,aim = connect_aim)    :
    """
        输入一个元组,左键点击给定的位置,可偏移
        clickpoint:tuple类型,点击的xy坐标
        x,y:int类型,xy坐标的偏移量
        return:None
    """
    if mode  == 0 :
        pyautogui.click(clickpoint[0] + changex,clickpoint[1] + changey,button='left')
    else :
        x = clickpoint[0] + changex
        y = clickpoint[1] + changey
        os.system(f'adb -s {aim} shell input touchscreen tap {x} {y}')#input touchscreen tap      adb shell input keyevent 4 返回

    return#click_change

def ocr_result(img_path = './imgs/screenshot.png') :
    """
        显示图片中所有识别到的结果
        img_path:str类型,图片地址(相对地址和绝对地址均可)
        return:list类型,包含paddleOCR返回的所有结果
    """
    result = ocr.ocr(img_path, cls=True)
    all_menmber = []
    
    for line in result:
        # print(line)    #调试用,查看所有识别结果和位置
        all_menmber.append(line[1][0])

    print('OCR结果',all_menmber)
    log_write('OCR结果为'+str(all_menmber)+'\n')
    return result#ocr_result

def ocr_extract(img_path = './imgs/screenshot.png') :
    """
        将OCR识别的结果提取出来
        result:list类型,ocr_result识别的结果
        return:list类型,
    """
    result = ocr.ocr(img_path, cls=True)
    all_menmber = []
    
    for line in result:
        all_menmber.append(line[1][0])

    print('OCR结果',all_menmber)
    log_write('OCR结果为'+str(all_menmber))
    return all_menmber#ocr_extract

def find_object(aim,img_path = './imgs/screenshot.png',touch=False) :
    """
        基于paddleOCR,找到目标的坐标
        aim:str类型,目标的名称
        img_path:str类型,图片地址,相对地址和绝对地址均可
        return:tuple类型,为目标的xy坐标
    """
    result = ocr.ocr(img_path, cls=True)
    
    for line in result:
        find_check = 0
        #print(line[1][0])
    
        if line[1][0] == aim :
            find_check = 1
            aim_location = ((line[0][0][0] + line[0][2][0]) / 2,(line[0][0][1] + line[0][2][1]) / 2)
            print('找到',line[1][0],aim_location)
            log_write('找到 '+aim+' '+str(aim_location))

    if find_check == 0 :
        return [False,(1,1)]

    if touch == True :
        click_change(aim_location)

    return [True,aim_location]#find_object

def get_xy(img_model_path,img_path = "./imgs/screenshot.png",touch = False,mode=0):
    """
        用来判定游戏画面的点击坐标
        img_model_path:用来检测的图片的文件名
        touch:bool类型,是否点击
        mode:int类型,0为返回图片中间坐标,1为返回左上角坐标,2为返回右下角坐标
        return:tuple类型,返回检测到的区域中心的坐标
    """
    img = cv2.imread(img_path)    # 待读取图像
    img_terminal = cv2.imread(f'./imgs/models/{img_model_path}.png')    # 图像模板
    height, width, channel = img_terminal.shape    # 读取模板的高度宽度和通道数
    result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)    # 使用matchTemplate进行模板匹配
    result_matrix = cv2.minMaxLoc(result)# 解析出匹配区域的左上角图标,最小值在前最大值在后
    print('精度:',result_matrix[1])
    log_write('精度'+str(result_matrix[1]))

    if result_matrix[1] < treshold :
        return [False,(1,1)]

    upper_left = result_matrix[3]    
    lower_right = (upper_left[0] + width, upper_left[1] + height)
    avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))    
    # 计算坐标的平均值并将其返回
    
    if touch == True :
        click_change(avg)
    
    if mode == 0:
        return [True,avg]
    elif mode == 1:
        return [True,upper_left]
    elif mode == 2:
        return [True,lower_right]#get_xy

def move_to(location) :
    pyautogui.moveTo(location[0],location[1],duration = 0.3)
    return#move_to

def get_mouse_location():
    """
        获取鼠标坐标
        return:tuple类型,包含鼠标的坐标
    """
    time.sleep(1)
    mouse_location = str(pyautogui.position())
    locationd = mouse_location.find(',')
    locationk = mouse_location.find(')')
    mousex = mousey = 0
    mousex = int(mouse_location[8:locationd])
    mousey = int(mouse_location[locationd + 4:locationk])
    print(mouse_location)
    return (mousex,mousey)#get_mouse_location

def adb_test() :
    if connect_mode == 1 :
        try :
            message = os.popen(f'adb connect {connect_aim}').read()
            # print(message)
            if f'already connected to {connect_aim}' in message :
                return True
        except UnicodeDecodeError :
            return False
    else :
        return True

if __name__ == 'main':
    try:
        if ocr_load == True:
            ocr = PaddleOCR(use_angle_cls=False, lang="ch")#加载OCR资源
            print('OCR初始化完成')
            log_write('OCR初始化完成')
    except IndentationError:
        ocr = PaddleOCR(use_angle_cls=False, lang="ch")#加载OCR资源
        print('OCR初始化完成')
        log_write('OCR初始化完成')