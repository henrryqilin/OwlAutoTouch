import cv2,os

from modules.dec_timer import average_timer,timer

class Template():

    def __init__(self,Template_DIR,Config,Father_scsh,Father_Butt):
        self.DIR = Template_DIR
        self.config = Config
        self.scsh = Father_scsh
        self.butt = Father_Butt

        self.read_mode = {}
        self.templates = {}
        self.last_result = []
        return

    # @timer
    def _match(self,Image,Template):
        height, width = Template.shape[0],Template.shape[1]	# 读取模板的高度宽度
        result = cv2.matchTemplate(Image, Template, cv2.TM_CCOEFF_NORMED)	# 使用matchTemplate进行模板匹配
        result_matrix = cv2.minMaxLoc(result)# 解析出匹配区域的左上角图标,最小值在前最大值在后
        return [result_matrix[3],result_matrix[1],height,width]
    
    # @timer
    def _location_calculate(self,Result,Forward_Mode):
        """
        Result:from func_match
        Forward_Mode:0:center,1:right_uper,2:left_uper,3:left_downer
        """
        if Result[1] < self.config['basic']["threshold"]:
            result = [False,(-1,-1)]
            return result
        
        if Forward_Mode == 0:
            result = [True,(int(Result[0][0] + Result[3] / 2),int(Result[0][1] + Result[2] / 2))]
        elif True:
            pass
        if self.butt.available_return() and self.zone_appear:
            up_left = self.butt.up_left()
            result = [True,(result[1][0] + up_left[0],result[1][1] + up_left[1])]
        return result

    @average_timer(t = 30)
    def get_xy(self,Template,Image = '',Colour_Mode = 1,Forward_Mode = 0):
        """
        Template:array/str,模版
        Image:array默认从截图实例中获取
        Colour_Mode = 1:默认为灰度,0:彩色,2带透明度通道(暂不支持)
        Forward_Mode = 0:0:center,1:right_uper,2:left_uper,3:left_downer
        """
        if len(self.templates) > 10:
            self.templates.clear()
        
        if type(Template) == str:
            if Template not in self.templates:
                self.templates[Template] = cv2.imread(os.path.join(self.DIR,'template',Template) + '.png',Colour_Mode)
            template = self.templates[Template]
            self.butt.tem_input(template,Template)
        else:
            template = Template
            self.butt.set_availabe()

        if Image == '':
            if Colour_Mode == 0:
                img = self.scsh.last_return()
            elif Colour_Mode == 1:
                img = self.scsh.gray_return()
            self.butt.img_input(img,self.scsh.last_return())
        elif type(Image) == str and ':' in Image:
            img = cv2.imread(Image,Colour_Mode)
            self.butt.img_input(img,Image)
        elif type(Image) == str and Image != '':# the image file is in /img
            img = cv2.imread(os.path.join(self.DIR,Image) + '.png',Colour_Mode)
            self.butt.img_input(img,Image)
        elif type(Image) != str:
            img = Image
        

        if self.butt.available_return():
            self.zone_appear = True
            result = self._match(self.butt.zone_return(),template)
            self.last_result = self._location_calculate(result,Forward_Mode)
            if not self.last_result[0]:
                self.zone_appear = False
                result = self._match(img,template)
                self.last_result = self._location_calculate(result,Forward_Mode)
        else:
            result = self._match(img,template)
            self.last_result = self._location_calculate(result,Forward_Mode)
        return self.last_result
    