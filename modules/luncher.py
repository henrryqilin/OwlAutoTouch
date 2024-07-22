import os,json

from modules.template import Template
from modules.button import Button_Manager
from modules.screenshot.screenshot import Screenshot

class Luncher():

    def __init__(self,DLC_Name):
        DIR = os.getcwd()
        self.DIR = os.path.join(DIR,'DLCS',DLC_Name)
        # print(os.listdir(self.DIR))

        # load json
        with open(os.path.join(self.DIR,DLC_Name + '.json'),encoding = 'utf-8') as f:
            self.config = json.loads(f.read())
            pass

        # system initialization
        self.butt = self.button_init()
        self.scsh = self.screenshot_init()
        self.temp = self.template_init()
        return
        
    def screenshot_init(self,DIR_Address = '',Father_Config = ''):
        if DIR_Address == '':
            DIR_Address = os.path.join(self.DIR,'imgs')
        if Father_Config == '':
            Father_Config = self.config
        return Screenshot(DIR_Address,Father_Config)

    def template_init(self,DIR_Address = '',Father_Config = '',Father_scsh = '',Father_Butt = ''):
        if DIR_Address == '':
            DIR_Address = os.path.join(self.DIR,'imgs')
        if Father_Config == '':
            Father_Config = self.config
        if Father_scsh == '':
            Father_scsh = self.scsh
        if Father_Butt == '':
            Father_Butt = self.butt
        return Template(DIR_Address,Father_Config,Father_scsh,Father_Butt)
    
    def button_init(self,DIR_Address = '',Father_Config = ''):
        if DIR_Address == '':
            DIR_Address = os.path.join(self.DIR,'imgs/template')
        if Father_Config == '':
            Father_Config = self.config
        return Button_Manager(DIR_Address,Father_Config)
    
    def config_check(self):
        check_list = ["developer_mode","default_shot","screenshot_interval","max_storage_capacity","threshold","OCR_use","retry_times"]
        return



if __name__ == '__main__':
    pass
