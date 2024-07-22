import time,os,cv2

from modules.dec_timer import average_timer,timer
from modules.screenshot.pyautogui import Pyautogui

class Screenshot():

    def __init__(self,Save_DIR,Config):
        self.DIR = Save_DIR
        self.config = Config

        self.screenshots = {}
        self.last_time = time.time()
        self.gray_name = 0
        self.gray_img = []

        self.shot_API = {}
        self.shot_API['pyautogui'] = Pyautogui()

        self.get_screen()
        return
    
    # @average_timer(t = 30)
    def get_screen(self,Mode = '',Interval = ''):
        if Mode == '':
            Mode = self.config['basic']["default_shot"]
        if Interval == '':
            Interval = self.config['basic']["screenshot_interval"]
        
        if len(self.screenshots) > (1.5 * self.config['basic']["max_storage_capacity"]):
            self.arrange()
        
        while time.time() - self.last_time < Interval:
            self.arrange()
            time.sleep(0.1)
        
        idcode = time.time()
        self.screenshots[str(idcode)] = self.shot_API[Mode].shot()
        self.last_time = idcode
        return self.screenshots[str(idcode)]
    
    # @timer
    def arrange(self):
        screenshot_amount = self.config['basic']["max_storage_capacity"]
        screenshot_list = list(self.screenshots.keys())
        screenshot_list.sort()

        while len(self.screenshots) > screenshot_amount:
            self.screenshots.pop(screenshot_list.pop(0))

        return
    
    def save(self):
        return
    
    def last_return(self):
        return self.screenshots[str(self.last_time)]
    
    def name_return(self):
        return str(self.last_time)

    def gray_return(self):
        if str(self.last_time) == self.gray_name:
            return self.gray_img
        
        self.gray_img = cv2.cvtColor(self.screenshots['{0}'.format(str(self.last_time))], cv2.COLOR_BGR2GRAY)
        self.gray_name = str(self.last_time)
        return self.gray_img