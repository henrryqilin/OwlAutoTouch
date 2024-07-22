import pyautogui,time,os,cv2

def get_screen(shot_change = None,mode = 0,save_path = 'D:/xiazheteng/OwlAutoTouch/DLCS/ZZZ/imgs',name='screenshot.png',):
        """
            截取屏幕
            shot_change:tuple类型,偏移的坐标,(x坐标,y坐标,x轴长度,y轴长度)
            save_location:str类型,截图保存的地址
            return:None
        """
        if mode == 0 :
            pyautogui.screenshot(region = shot_change).save(os.path.join(save_path,name))
        return#get_screen

def get_xy(img_model_path,img_path = "D:/xiazheteng/OwlAutoTouch/DLCS/ZZZ/imgs/screenshot.png",touch = False,mode=0):
    """
	    用来判定游戏画面的点击坐标
	    img_model_path:用来检测的图片的文件名
	    touch:bool类型,是否点击
	    mode:int类型,0为返回图片中间坐标,1为返回左上角坐标,2为返回右下角坐标
	    return:tuple类型,返回检测到的区域中心的坐标
	"""
    img = cv2.imread(img_path,1)	# 待读取图像
    print(img)
    img_terminal = img_model_path	# 图像模板b
    height, width = img_terminal.shape[0],img_terminal.shape[1]	# 读取模板的高度宽度和通道数
    result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)	# 使用matchTemplate进行模板匹配
    result_matrix = cv2.minMaxLoc(result)# 解析出匹配区域的左上角图标,最小值在前最大值在后
    print('精度:',result_matrix[1])
    
    if result_matrix[1] < 0.85 :
        return [False,(1,1)]

    upper_left = result_matrix[3]    
    lower_right = (upper_left[0] + width, upper_left[1] + height)
    avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2)) 
    return [True,avg]


if __name__ == '__main__':
    img = cv2.imread('D:/xiazheteng/OwlAutoTouch/DLCS/ZZZ/imgs/cancel.png',1)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    print(img)
    while True:
        # time.sleep(4)
        # pyautogui.click(827,645,button='left')
        # time.sleep(4)
        while True:
            # get_screen()
            print('开始')
            result = get_xy(img)
            if result[0]:
                pyautogui.click(result[1][0],result[1][1],button='left')
                break