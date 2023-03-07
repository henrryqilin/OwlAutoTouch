import time,cv2
from basic import get_screen,click_change,find_object,get_xy,log_write

class Auto_combat(list) :

    def __init__(self) :
        self.character = 'jinran'
        self.last = None
        self.passive = None
        self.next = None
 
    def refresh(self,img_path = './imgs/screenshot.png') :
        self.clear()
        red = cv2.imread(f'./imgs/models/actors/{self.character}/red.png')
        yellow = cv2.imread(f'./imgs/models/actors/{self.character}/yellow.png')
        blue = cv2.imread(f'./imgs/models/actors/{self.character}/blue.png')
        img = cv2.imread(img_path)
        
        for i in range(8) :
            ball = img[709:819,1774 - i * 162:1884 - i * 162]# 切割
            # cv2.imwrite(f'./imgs/develop/ball{i}.png', ball,[cv2.IMWRITE_PNG_COMPRESSION, 0])#保存
            result = cv2.matchTemplate(ball, red, cv2.TM_CCOEFF_NORMED)	# 读取红黄蓝模板
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
        log_write(str(self)+'\n')
        dev_list = self.copy()
        dev_list.reverse()
        print(dev_list)
        log_write('反转'+str(dev_list)+'\n')

    def highest(self) :
        if self == [] :
            self.next = None
            self.last = None
            print('无技能球')
            log_write('无技能球')
            return

        highest_score = 0.0

        for i in range(len(self)) :
            score = 0.0
            # print('分数清零','+0',score)
            log_write('分数清零 '+'+0 '+str(score))
            next = self.copy()
            
            if i < len(self) - 1 :
                if self[i] == self[i + 1] :
                    score -= 0.3
                    # print('双消','-0.3',score)
                    log_write('双消 '+'-0.3 '+str(score))
                    if i < len(self) - 2 :
                        if self[i] == self[i + 1] == self[i + 2] :
                            score += 3
                            # print('三消','+3',score)
                            log_write('三消 '+'+3 '+str(score))
                            next.remove(next[i + 2])
                    next.remove(next[i + 1])
            
            score += 1
            # print('单消','+1',score)
            log_write('单消 '+'+1 '+str(score))
            next.remove(next[i])
            # print(next)
            log_write(str(next))
            n = 0
            last = 0
            residue_two = 0
            residue_three = 0
            
            for each in next :
                if last == each :
                    n += 1
                    if n >= 2 :
                        residue_two += 1
                        if n == 3 :
                            residue_two -= 2
                            residue_three += 1
                            n = 0
                else :
                    n = 0
                last = each
            
            print('原有',f'{residue_three}个三消',f'{residue_two}个双消')
            log_write('原有'+f'{residue_three}个三消'+f'{residue_two}个双消')
            
            for line in range(len(next)) :
                if line < len(next) - 2 :
                    if next[line] == next[line + 1] == next[line + 2] and next[line] != 0:
                        score = score + 6 -n * 6
                        print('创三消',f'+{6-residue_three*6}',score)
                        log_write('创三消 '+f'+{6-residue_three*6} '+str(score))
                        next[line] = 0
                        next[line + 1] = 0
                        next[line + 2] = 0
                
                if line < len(next) - 1 :
                    if next[line] == next[line + 1] == 'r' \
                    or next[line] == next[line + 1] == 'y' \
                    or next[line] == next[line + 1] == 'b' \
                    and next[line] != 0 :
                        score = score + 2 - residue_two * 2
                        print('创双消',f'+{2-residue_two*2}',score)
                        log_write('创双消 '+f'+{2-residue_two*2} '+str(score))
                        next[line] = 0
                        next[line + 1] = 0
                
            
            print(next,score,f'消{i} ')
            log_write(str(next)+''+str(score)+''+f'消{i}'+'\n')
            
            if score > highest_score :
                highest_score = score

                self.next = i
            
        print('应点击',self[int(self.next)],self.next)
        log_write('应点击'+' '+str(self[int(self.next)])+' '+str(self.next))


a = Auto_combat()
a.refresh(img_path = './imgs/develop/screenshot09.png')
a.highest()
