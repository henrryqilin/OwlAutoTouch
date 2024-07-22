import cv2,pyautogui,time,os
# from paddleocr import PaddleOCR

# with open('./modules/setting.json',mode='r',encoding='utf-8') as f:#
#     setting=eval(f.read())

def log_organize():
    log_list = os.listdir(path='./logs')#整理logs文件夹中的日志文件
    log_list.sort(reverse = True)
    # print(log_list)

    if len(log_list) > setting['basic']['logs_quantity'] :

        for i in log_list[setting['basic']['logs_quantity']:len(log_list)] :
            os.remove(f'./logs/{i}')

    log_time = time.strftime("%Y-%m-%d %H.%M.%S",time.localtime())#创建本次运行日志文件
    log = open(f'./logs/{log_time}.txt','w',encoding = 'utf-8')
    log.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+' 开始运行\n')
    log.close()

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

class ocr_recognition(dict):

    def __init__(self,package_name=None):
        self.ocr=PaddleOCR(use_angle_cls=True, lang="ch")
        try:
            package=package_name.split('.')
            print(f'{package[-1]}_correct.json')
            f=open(f'./modules//{package[-1]}/{package[-1]}_correct.json',mode='r',encoding='utf-8')
            self.correct_dict=eval(f.read())
            if len(self.correct_dict) > 0:
                self.correct_mode=True
            else:
                self.correct_mode=False
        except FileNotFoundError:
            print('{:-^50}'.format('FileNotFoundError 未找到correect字典文件'))
            self.correct_mode=False
        
        self.result('./imgs/models/OCR初始化.png')

    def correction(self,pending_str):
        """
        纠正ocr识别中可能出现的错误
        pending_str:str,可能需要纠正的字符串,如果不是字符串则会返回原值
        mode:bool,用于判定是否需要
        return:str,原值或原值在字典中对应的值
        """
        if type(pending_str) != type(' '):
            print('WARNING:The input type is not \'str\'')
            return pending_str
        value=self.correct_dict.get(pending_str)
        if value != None:
            return value
        else:
            return pending_str

    def result(self,img_path='./imgs/screenshot.png'):
        """
        将OCR识别的结果提取出来
        img_path:str,目标图片的位置
        result:dict类型,ocr_result识别的结果和对应的坐标
        return:未处理的ocr识别结果
        """
        self.clear()
        result = self.ocr.ocr(img_path, cls=True)
        
        if self.correct_mode == False:
            for line in result:
                self[line[1][0]]=((line[0][0][0] + line[0][2][0]) / 2,(line[0][0][1] + line[0][2][1]) / 2)
        else:
            for line in result:
                self[self.correction(pending_str=line[1][0])]=((line[0][0][0] + line[0][2][0]) / 2,(line[0][0][1] + line[0][2][1]) / 2)
        log_write('OCR结果为'+str(list(self.keys())))
        print(self)
        return result#ocr_extract
    
    # @get_time
    def find(self,dim_aim):
        """
        调用result后,获取目标的坐标,有简单的模糊搜索
        dim_aim:str,目标
        return:tuple,(是否找到,(坐标))
        """                
        if dim_aim in self:
            return (True,self.get(dim_aim))
        
        else:
            for i in self:
                # print(i)
                # print(self.keys())
                if dim_aim in i:
                    other=False

                    for line in list(self.keys()).remove(i):
                        if dim_aim in line:
                            aim=dim_aim
                            other=True
                            break
                    
                    if other == False:    
                        aim=i
                        return (True,self.get(aim))
            return (False,(-1,-1))

class img_recognition(dict):

    def __init__(self,package_name=''):
        self.last=None
        self.model=None
        self.package=package_name.split('.')[-1]
        print(self.package)

    # @get_time
    def get_xy(self,img_model,folder='',img_path = "./imgs/screenshot.png",touch = False,mode=0,tres=setting['basic']['treshold']):
        """
        用来寻找游戏画面中图片的坐标
        img_model_list:用来检测的图片的文件名,不带后缀,格式为:xxx或xxx(文件夹)/xxx(图片名)
        touch:bool类型,是否点击
        mode:int类型,0为返回图片中间坐标,1为返回左上角坐标,2为返回右下角坐标
        return:tuple,(Ture,(坐标x,坐标y))/(False,(-1,-1))
        """
        self.clear()
        img = cv2.imread(img_path)    # 待检测图像
        
        if type(img_model) == type(list()):
            for i in img_model:
                if len(img_model) > 1:#多图
                    if self.last != img_model[0]:
                        img_terminal = cv2.imread(f'./imgs/models/{folder}{i}.png')    # 图像模板
                        height, width, channel = img_terminal.shape    # 读取模板的高度宽度和通道数
                        result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)    # 使用matchTemplate进行模板匹配
                        result_matrix = cv2.minMaxLoc(result)# 从矩阵中解析出匹配区域的左上角图标,最小值在前最大值在后
                        print('精度:',result_matrix[1])
                        log_write('精度'+str(result_matrix[1]))

                        if result_matrix[1] < tres :
                            self[i]=(False,(-1,-1))
                            continue

                        upper_left = result_matrix[3]    
                        lower_right = (upper_left[0] + width, upper_left[1] + height)
                        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))    
                        # 计算坐标的平均值并将其返回
                            
                        if touch == True :
                            shot_tap.click_change(avg)
                            
                        if mode == 0:
                            self[i]=(True,avg)
                        elif mode == 1:
                            self[i]=(True,upper_left)
                        elif mode == 2:
                            self[i]=(True,lower_right)

                elif len(img_model) == 1:#单图
                    if self.last == img_model[0]:#相同
                        height, width, channel = self.model.shape    # 读取模板的高度宽度和通道数
                        result = cv2.matchTemplate(img, self.model, cv2.TM_CCOEFF_NORMED)
                    else:#不同
                        self.model=img_terminal = cv2.imread(f'./imgs/models/{folder}{img_model[0]}.png')    # 图像模板
                        height, width, channel = img_terminal.shape    # 读取模板的高度宽度和通道数
                        result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)    # 使用matchTemplate进行模板匹配
        elif type(img_model) == type(str()):
            if self.last == img_model:#相同
                height, width, channel = self.model.shape    # 读取模板的高度宽度和通道数
                result = cv2.matchTemplate(img, self.model, cv2.TM_CCOEFF_NORMED)
            else:#不同
                self.model=img_terminal = cv2.imread(f'./imgs/models/{folder}{img_model}.png')    # 图像模板
                height, width, channel = img_terminal.shape    # 读取模板的高度宽度和通道数
                result = cv2.matchTemplate(img, img_terminal, cv2.TM_CCOEFF_NORMED)    # 使用matchTemplate进行模板匹配

        if len(img_model) == 1 or type(img_model) == type(str()):
            result_matrix = cv2.minMaxLoc(result)# 从矩阵中解析出匹配区域的左上角图标,最小值在前最大值在后
            print('精度:',result_matrix[1])
            log_write('精度'+str(result_matrix[1]))

            upper_left = result_matrix[3]    
            lower_right = (upper_left[0] + width, upper_left[1] + height)
            avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))    
            # 计算坐标的平均值并将其返回

            if type(img_model) == type(str()):
                if result_matrix[1] < tres :
                    self[img_model]=(False,(-1,-1))
                    print(self)
                    return
                    
                if touch == True :
                    shot_tap.click_change(avg)
                                
                if mode == 0:
                    self[img_model]=(True,avg)
                elif mode == 1:
                    self[img_model]=(True,upper_left)
                elif mode == 2:
                    self[img_model]=(True,lower_right)
            
            elif type(img_model) == type(list()):

                if result_matrix[1] < tres :
                    self[img_model[0]]=(False,(-1,-1))
                    print(self)
                    return
                    
                if touch == True :
                    shot_tap.click_change(avg)
                                
                if mode == 0:
                    self[img_model[0]]=(True,avg)
                elif mode == 1:
                    self[img_model[0]]=(True,upper_left)
                elif mode == 2:
                    self[img_model[0]]=(True,lower_right)
        print(self)
        log_write(str(self))

class shot_tap():

    def __init__(self,interval=setting['basic']['shot_interval']):
        self.last_shot=time.time()
        self.shot_time=0
        self.interval=interval
    
    def get_screen(self,shot_change = None,mode = setting['basic']['connect_mode'],save_path = './imgs/',name='screenshot.png',
        aim = setting['basic']['connect_aim']):
        """
            截取屏幕
            shot_change:tuple类型,偏移的坐标,(x坐标,y坐标,x轴长度,y轴长度)
            save_location:str类型,截图保存的地址
            return:None
        """
        while True:
            if time.time() - self.last_shot > self.interval:
                break
            else:
                time.sleep(0.2)

        if mode == 0 :
            pyautogui.screenshot(region = shot_change).save(save_path+name)
        else :
            os.system(f'adb -s {aim} shell screencap -p /sdcard/{name}')
            os.system(f'adb -s {aim} pull sdcard/{name} {save_path}')
        self.last_shot=time.time()
        self.shot_time+=1
        return#get_screen
    
    def click_change(self,clickpoint,change=(0,0),mode = setting['basic']['connect_mode'],aim = setting['basic']['connect_aim'])    :
        """
            输入一个元组,左键点击给定的位置,可偏移
            clickpoint:tuple类型,点击的xy坐标
            x,y:int类型,xy坐标的偏移量
            return:None
        """
        if mode  == 0 :
            pyautogui.click(clickpoint[0] + change[0],clickpoint[1] + change[1],button='left')
        else :
            x = clickpoint[0] + change[0]
            y = clickpoint[1] + change[1]
            os.system(f'adb -s {aim} shell input touchscreen tap {x} {y}')#input touchscreen tap      adb shell input keyevent 4 返回

        self.shot_time=0
        return#click_change
