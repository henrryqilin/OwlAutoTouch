import time,cv2
from basic import get_screen,click_change,find_object,get_xy,log_write

class Ball(list) :

    def __init__(self) :
        self.last = None
        self.passive = None
        self.next = None

    
    def refresh(self,img_path = './imgs/screenshot.png',character = 'jinran') :
        self.clear()
        red = cv2.imread(f'./imgs/models/{character}/red.png')
        yellow = cv2.imread(f'./imgs/models/{character}/yellow.png')
        blue = cv2.imread(f'./imgs/models/{character}/blue.png')
        img = cv2.imread(img_path)
        
        for i in range(8) :
            ball = img[709:819,1774 - i * 162:1884 - i * 162]
            # cv2.imwrite(f'./imgs/ball{i}.png', ball,[cv2.IMWRITE_PNG_COMPRESSION, 0])
            result = cv2.matchTemplate(ball, red, cv2.TM_CCOEFF_NORMED)	# 使用matchTemplate进行模板匹配（标准平方差匹配）
            red_matrix = cv2.minMaxLoc(result)
            result = cv2.matchTemplate(ball, yellow, cv2.TM_CCOEFF_NORMED)	
            yellow_matrix = cv2.minMaxLoc(result)
            result = cv2.matchTemplate(ball, blue, cv2.TM_CCOEFF_NORMED)	
            blue_matrix = cv2.minMaxLoc(result)
            # print(red_matrix[1],yellow_matrix[1],blue_matrix[1])
            
            if red_matrix[1] > 0.65 :
                self.append('r')
            elif yellow_matrix[1] > 0.65 :
                self.append('y')
            elif blue_matrix[1] > 0.65 :
                self.append('b')

        print(self)

    def highest(self) :
        highest_score = 0.0
        
        for i in range(len(self)) :
            score = 0.0
            next = self.copy()
            
            if i > len(self) - 2 :
                if self[i] == self[i + 1] == self[i + 2] :
                    score += 2
                    next.remove(next[i + 1])
                    next.remove(next[i + 2])
            
            score += 1
            next.remove(next[i])
            
        pass

# a = Ball()
# a.refresh(img_path = './imgs/develop/screenshot5.png')
