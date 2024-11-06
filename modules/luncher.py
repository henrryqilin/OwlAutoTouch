import os,json

from modules.logger import Logger
from modules.template import Template
from modules.button import Button_Manager
from modules.screenshot.screenshot import Screenshot

class Luncher():

    def __init__(self,DLC_Name,Resource_Reference = {}):
        self.configs = {}

        DIR = os.getcwd()
        self.DIR = os.path.join(DIR,'DLCS',DLC_Name)
        self.configs['dir'] = self.DIR
        # print(os.listdir(self.DIR))

        # load json
        try:
            with open(os.path.join(self.DIR,DLC_Name + '.json'),encoding = 'utf-8') as f:
                self.config = self.configs['config'] = json.load(f)
        except:
            pass
        
        # system initialization
        self.configs['logg'] = Logger(self.configs)
        self.configs['butt'] = Button_Manager(self.configs)
        self.configs['scsh'] = Screenshot(self.configs)
        self.configs['temp'] = Template(self.configs)

        return
    
    def config_check(self):
        check_list = ["developer_mode","default_shot","screenshot_interval","max_storage_capacity","threshold","OCR_use","retry_times"]
        return



if __name__ == '__main__':
    pass
