import cv2,time
from basic import get_screen,click_change,ocr_result,ocr_extract,find_object,get_xy,log_write,adb_test

adb_test()

while True:
    while True:
        get_screen()
        if '放弃' in ocr_extract():
            find_object('放弃',touch=True)
        if '将会以当前进度结算游戏' in ocr_extract():
            get_xy('yes',touch=True)
        if get_xy('back',touch=True)[0]:
            pass
        if get_xy('start',touch=False)[0]:
            break
    
    while True:
        get_screen()
        if get_xy('start',touch=True)[0]:
            pass
        if '请点击进行编队初始化' in ocr_extract():
            break
    
    while True:
        get_screen()
        ocrocr=ocr_extract()
        if get_xy('chushihua',touch=True)[0]:
            pass
        if '全队补充' in ocrocr:
            find_object('全队补充',touch=True)
        if '演算开始' in ocrocr:
            find_object('演算开始',touch=True)
        if '今日日报' in ocrocr:
            find_object('今日日报',touch=True)
        if '决断' in ocrocr:
            break
    
    while True:
        get_screen()
        ocrocr=ocr_extract()
        if get_xy('gongzuotai',touch=True)[0]:
            continue
        if get_xy('xiexie',touch=True)[0]:
            continue
        if '蟹蟹抽水泵' in ocrocr:
            find_object('开始组装',touch=True)
            break

    while True:
        get_screen()

