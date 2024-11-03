import os,json,cv2

class Button_Manager():

    def __init__(self,Config_Input):
        self.DIR = Config_Input['dir']
        self.config = Config_Input['config']

        self.available = False
        self.register_list = {}
        self.img_name = None
        self.template = None
        self.enlarge_parameter = ()
        return
    
    def tem_input(self,Template,Name):
        if type(Name) != str:
            self.available = False
            return
        
        try:
            if Name not in self.register_list:
                with open('{0}'.format(os.path.join(self.DIR,os.path.dirname(Name),'register_list.json')),mode = 'r',encoding = 'utf-8') as f:
                    self.register_list = json.load(f)
            self.enlarge_parameter = (tuple(self.register_list[Name]['expect']),self.register_list[Name]['zoom'])# 这里叫放大参数其实有点抽象
        except FileNotFoundError:
            self.available = False
            return
        except json.JSONDecodeError or KeyError:
            self.available = False
            print('请检查json文件格式情况')
            return
        
        if Name in self.register_list:
            self.available = True
        self.height,self.width = Template.shape[0],Template.shape[1]
        
        return
    
    def img_input(self,Image,Name):
        if not self.available:
            return
        if Name != self.img_name:
            self.img = Image
            self.img_name = Name
            return
        
        return
    
    def zone_return(self):# 注:此处的坐标为模板出现的中心坐标,这样才方便结算出左上角坐标
        if self.available:
            self.upper_left = (int(self.enlarge_parameter[0][0] - (self.width * self.enlarge_parameter[1]) / 2),int(self.enlarge_parameter[0][1] - (self.height * self.enlarge_parameter[1]) / 2))
            image = self.img[self.upper_left[1]:int(self.upper_left[1] + self.height * self.enlarge_parameter[1]),self.upper_left[0]:int(self.upper_left[0] + self.width * self.enlarge_parameter[1])]
            return image
        else:# is impossible
            return
    
    def _imcut(self,Image,X,Y,Height,Width):
        return Image[Y:Y + Height,X:X + Width]

    def available_return(self):
        return self.available
    
    def set_available(self,Available = False):
        self.available = Available
        return

    def up_left(self):
        return self.upper_left
    