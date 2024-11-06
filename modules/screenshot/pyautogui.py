import numpy as np
import pyscreeze,json,cv2

from modules.dec_timer import average_timer,timer

class Pyautogui():

    def __init__(self):
        return
    
    # @average_timer(t = 30)
    def shot(self):
        return cv2.cvtColor(np.asarray(pyscreeze.screenshot()),cv2.COLOR_RGB2BGR)
    

if __name__ == '__main__':
    pass