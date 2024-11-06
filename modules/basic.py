import cv2,pyautogui,time,os
# from paddleocr import PaddleOCR
# from modules.dec_timer import timer


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

class omnipotent_tool(dict):

    # @timer
    def __init__(self,Package_Name):
        self.i={}
        self.o={}

        self.package_name=Package_Name.split('.')[-1]
        print(self.get_config())
        self.get_config(self.package_name)

        self.log_create = self.log_organize()
        self.log_write(str(self.package_name))
        
        # self.ocr_module=PaddleOCR(use_angle_cls=False, lang="ch")#载入ocr模型
        try:#尝试载入correct.json
            package=Package_Name.split('.')
            print(f'{package[-1]}_correct.json')
            f=open(f'./modules/{self.package_name}/{self.package_name}_correct.json',mode='r',encoding='utf-8')
            self.correct_dict=eval(f.read())
            if len(self.correct_dict) > 0:
                self.correct_mode=True
            else:
                self.correct_mode=False
        except FileNotFoundError:
            print('{:-^50}'.format('FileNotFoundWarning 未找到correect字典文件'))
            self.log_write('FileNotFoundWarning 未找到correect字典文件')
            self.correct_mode=False
        
        self.result('./imgs/models/OCR初始化.png')#ocr初始化,加快后续识别速度
        self.log_write('OCR初始化完成')

        self.last=None
        self.model=None
        self.log_write('opencv初始化完成')

        self.last_shot=time.time()
        self.shot_time=0
        self.log_write('screenshot初始化完成')

        self.log_write('omnipotent_tool初始化完成')
    
    def get_config(self,Config_Tags=''):
        if Config_Tags == '':
            Config_Tags=self.package_name
        try:
            with open(f'./modules/{Config_Tags}/config.json',mode='r',encoding='utf-8') as f:
                setting=eval(f.read())
        except FileNotFoundError:
            print('ERROR:File config is not found.')
            pass
        return setting
    
    def log_organize(self):
        aim_list=[]
        log_list = os.listdir(path='./logs')#整理logs文件夹中的日志文件
        
        for i in range(len(log_list)):
            if f'{self.package_name} ' in log_list[i]:
                aim_list.append(log_list[i])
        aim_list.sort(reverse = True)
        
        if len(aim_list) > self.get_config()['basic']["logs_quantity"]:
            
            for i in range(len(aim_list)-self.get_config()['basic']["logs_quantity"]):
                os.remove(f'./logs/{aim_list[i]}')
        log_time = time.time()#创建本次运行日志文件
        self.log_name = "{0} {1}".format(self.package_name,time.strftime("%Y-%m-%d %H.%M.%S",time.localtime(log_time)))
        log = open(f'./logs/{self.log_name}.txt','w',encoding = 'utf-8')
        log.close()

        return log_time
    
    def log_write(self,log_Text):
        if time.time() - self.log_create > 600:#如果当前时间与创建日志时间相差大于10分钟，则重新创建日志文件
            self.log_create = self.log_organize()
        
        log = open(f'./logs/{self.log_name}.txt','a',encoding = 'utf-8')
        log.write((time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+' '+str(log_Text)+'\n'))
        log.close()
        return

    def template(self,Name,Model,Img,Mode):
        if Name != self.last:
            img_terminal = cv2.imread(Model)    # 图像模板
            height, width, channel = img_terminal.shape    # 读取模板的高度宽度和通道数
            self.model=img_terminal
        else:
            img_terminal = self.model
            height, width, channel = self.model.shape
        result = cv2.matchTemplate(Img, img_terminal, cv2.TM_CCOEFF_NORMED)    # 使用matchTemplate进行模板匹配
        result_matrix = cv2.minMaxLoc(result)# 从矩阵中解析出匹配区域的左上角图标,最小值在前最大值在后
        #-----
        # print(result_matrix)
        #-----
        upper_left = result_matrix[3] 
        self.log_write(str(Name)+' 模板匹配精度:'+str(result_matrix[1])+str(result_matrix[3]))

        if result_matrix[1] < self.get_config()['basic']["treshold"] :
            self.i[Name]=(False,(-1,-1))
            return

        if Mode == 0:
            self.i[Name]=(True,(int((upper_left[0] + width) / 2), int((upper_left[1] + height) / 2)))
        elif Mode == 1:
            self.i[Name]=(True,upper_left)
        elif Mode == 2:
            self.i[Name]=(True,(upper_left[0] + width, upper_left[1] + height))
        return
    
    def get_xy(self,Models,Img_Path = "",Special_Module='',Mode=0):
        self.clear()
        if Img_Path == '':
            Img_Path = f'./modules/{self.package_name}/imgs/screenshot.png'
        img=cv2.imread(Img_Path)

        if Special_Module != '':
            self.template(Special_Module,Special_Module,img,Mode)

        if type(Models) == type([]):
            for i in Models:
                self.template(i,f'./modules/{self.package_name}/imgs/{i}.png',img,Mode)
        elif type(Models) == type(''):
            self.template(Models,f'./modules/{self.package_name}/imgs/{Models}.png',img,Mode)
        
        return
    
    def correction(self,Pending_Str):
        """
        纠正ocr识别中可能出现的错误
        pending_str:str,可能需要纠正的字符串,如果不是字符串则会返回原值
        mode:bool,用于判定是否需要
        return:str,原值或原值在字典中对应的值
        """
        if type(Pending_Str) != type(' '):
            print('WARNING:The input type is not \"str\"')
            return Pending_Str
        value=self.correct_dict.get(Pending_Str)
        if value != None:
            self.log_write(f'将 {Pending_Str} 替换为 {value}')
            return value
        else:
            return Pending_Str

    def result(self,Img_Path=''):
        """
        将OCR识别的结果提取出来
        img_path:str,目标图片的位置
        result:dict类型,ocr_result识别的结果和对应的坐标
        return:未处理的ocr识别结果
        """
        self.clear()
        if Img_Path == '':
            Img_Path = f'./modules/{self.package_name}/imgs/screenshot.png'
        result = self.ocr_module.ocr(Img_Path, cls=False)
        
        if self.correct_mode == False:
            for line in result:
                self.o[line[1][0]]=((line[0][0][0] + line[0][2][0]) / 2,(line[0][0][1] + line[0][2][1]) / 2)
        else:
            for line in result:
                self.o[self.correction(pending_str=line[1][0])]=((line[0][0][0] + line[0][2][0]) / 2,(line[0][0][1] + line[0][2][1]) / 2)
        self.log_write(f'OCR:'+str(self.o))
        return
    
    def get_screen(self,shot_change = None,save_path = ''):
        """
            截取屏幕
            shot_change:tuple类型,偏移的坐标,(x坐标,y坐标,x轴长度,y轴长度)
            save_location:str类型,截图保存的地址
            return:None
        """
        if save_path == '':
            save_path = f'./modules/{self.package_name}/imgs/screenshot.png'
        
        interval=self.get_config()['basic']["shot_interval"]
        while True:
            a=time.time() - self.last_shot
            if a > interval or a < 0:
                break
            else:
                time.sleep(0.2)

        if self.get_config()['basic']['connect_mode'] == 0 :
            pyautogui.screenshot(region = shot_change).save(save_path)
        else :
            name = save_path.split('/')[-1]
            path = save_path.replace('/' + name,'')
            aim = self.get_config()['basic']['connect_aim']
            os.system(f'adb -s {aim} shell screencap -p /sdcard/{name}')
            os.system(f'adb -s {aim} pull sdcard/{name} {path}')
        self.last_shot=time.time()
        self.shot_time+=1
        return#get_screen
    
    def click_change(self,clickpoint,change=(0,0)):
        """
            输入一个元组,左键点击给定的位置,可偏移
            clickpoint:tuple类型,点击的xy坐标
            x,y:int类型,xy坐标的偏移量
            return:None
        """
        if self.get_config()['basic']['connect_mode']  == 0 :
            pyautogui.click(clickpoint[0] + change[0],clickpoint[1] + change[1],button='left')
        else :
            aim = self.get_config()['basic']['connect_aim']
            x = clickpoint[0] + change[0]
            y = clickpoint[1] + change[1]
            os.system(f'adb -s {aim} shell input touchscreen tap {x} {y}')#input touchscreen tap      adb shell input keyevent 4 返回

        self.shot_time=0
        return#click_change

    def adb_test(self):
        """
        进行adb连接测试
        return:bool,是否测试通过,通过为True
        """
        if self.get_config()['basic']['connect_mode'] == 1 :
            try :
                message = os.popen(f'adb connect {0}'.format(self.get_config()['basic']['connect_aim'])).read()
                # print(message)
                if f'already connected to {0}'.format(self.get_config()['basic']['connect_aim']) in message :
                    return True
            except UnicodeDecodeError :
                return False
        else :
            return True
