#coding=utf-8

list1=['suit','seat','level','main_tag','secondary_tag','locked','owner']
list2=['+0','+1','+2','+3','+4','+5','+6','+7','+8','+9','+10','+11','+12','+13','+14','+15','+16','+17','+18','+19','+20']
seat_list=['生之花','死之羽','时之沙','空之杯','理之冠']
tag_list=['攻击力','生命值','防御力','元素精通','暴击率','暴击伤害','元素充能效率','物理伤害加成','治疗加成',
          '火元素伤害加成','水元素伤害加成','雷元素伤害加成','冰元素伤害加成','风元素伤害加成','岩元素伤害加成','草元素伤害加成']
suit_dict={'乐园遗落之花':'乐园'}

import time,cv2,pyautogui,os
from modules.basic import omnipotent_tool


class relic_rec(omnipotent_tool):

    def __init__(self):
        
        self.relic_list=[]
        for i in os.listdir('./imgs/models/genshen'):
            self.relic_list.append(i.replace('.png',''))
        print(self.relic_list)

    def division_recognize(self,):
        ot.get_screen()
        self.clear()
        self=dict.fromkeys(list1)
        print(self)
        ot.get_xy(['five_star'],mode=1)
        img=cv2.imread('./imgs/screenshot.png')
        screenshot_p1=img[:ot.i['five_star'][1][1],ot.i['five_star'][1][0]:]
        cv2.imwrite('./imgs/p1.png', screenshot_p1,[cv2.IMWRITE_PNG_COMPRESSION,0])
        screenshot_p2=img[ot.i['five_star'][1][1]:,ot.i['five_star'][1][0]:]
        cv2.imwrite('./imgs/p2.png', screenshot_p2, [cv2.IMWRITE_PNG_COMPRESSION,0])
        del img,screenshot_p1,screenshot_p2
        ot.result('./imgs/p1.png')
        
        for i in ot.o:#上半图片信息
            if i in seat_list:
                if i == '生之花':
                    self['seat']=1
                elif i == '死之羽':
                    self['seat']=2
                elif i == '时之沙':
                    self['seat']=3
                elif i == '空之杯':
                    self['seat']=4
                elif i == '理之冠':
                    self['seat']=5
            elif i in tag_list:
                for line in ot.o:
                    if line.isascii():
                        if i =='攻击力' or i == '生命值' or i == '防御力' and '%'in line:
                            self['main_tag']=(i+'百分比',float(line.replace(',','').replace('%','')))                        
                        elif i =='攻击力' or i == '生命值' or i == '防御力' and '%' not in line:
                            self['main_tag']=(i,float(line.replace(',','').replace('%','')))
        ot.result('./imgs/p2.png')
        ot.get_xy('unlocked',img_path='./imgs/p2.png')
        
        if ot.i['unlocked'][0]:
            self['locked']=False
        else:
            self['locked']=True
        self['secondary_tag']=list()
        
        for i in ot.o:
            if '+' in i:
                if i.isascii():
                    self['level']=int(i.split('+')[-1])
                else:
                    x=i.split('+')
                    
                    if x[0].replace('·','') in tag_list:
                        if i =='攻击力' or i == '生命值' or i == '防御力' and '%'in i:
                            self['secondary_tag'].append((x[0].replace('·','')+'百分比',float(x[-1].replace(',','').replace('%',''))))
                        else:
                            self['secondary_tag'].append((x[0].replace('·',''),float(x[-1].replace(',','').replace('%',''))))
            elif '已装备' in i:
                self['owner']=i.split('已装备')[0]
            elif i.replace('：','').replace(':','') in suit_dict:
                self['suit']=suit_dict.get(i.replace('：','').replace(':',''))
        print(self)

    def next_i(self):
        for i in self.relic_list:
            irec.get_xy(i,folder='genshen/',img_path='./imgs/this_page.png',tres=0.7)
            
            if irec[i][0] == True:
                click_change(irec[i][1])
                break
        
        if list(irec.values())[0][0] == False:
            return False
        img=cv2.imread('./imgs/this_page.png')
        cv2.circle(img,irec[i][1],50,(0,255,0),-1)
        cv2.imwrite(f'./imgs/this_page.png',img,[cv2.IMWRITE_PNG_COMPRESSION, 0])
        return True

    def next_o(self):
        result=orec.result('./imgs/this_page.png')
        irec.get_xy(['five_star'],mode=1)
        find=False
        
        for i in result:
            # print(i)
            if i[1][0] in list2 and i[0][0][0] < irec['five_star'][1][0]:
                location=(int((i[0][0][0]+i[0][2][0])/2),int((i[0][0][1]+i[0][2][1])/2))
                print(location,'我进来了')
                click_change(location)
                find=True
                break
        
        if find == True:
            img=cv2.imread('./imgs/this_page.png')
            cv2.circle(img,location,50,(0,255,0),-1)
            cv2.imwrite(f'./imgs/this_page.png',img,[cv2.IMWRITE_PNG_COMPRESSION, 0])
            return True
        else:
            return False
    
    def record(self):
        f=open('./modules/genshen.txt',mode='a',encoding='utf-8')
        
        for i in self:
            if i == 'main_tag':
                f.write('{:^20}'.format(self[i]+','))
            elif i == 'secondary_tag':
                f.write('{:^20}'.format(self[i]+','))
            else:
                f.write(str(self[i])+',')
        f.write('\n')
        f.close()

def master():
    ot = omnipotent_tool(__name__)

    while True:
        shot.get_screen()
        irec.get_xy(['bag','bag_relic','bag_others'])

        if irec['bag'][0] == True and irec['bag'][1][0] > 500:
            pyautogui.press('b')
        elif irec['bag_others'][0] == True:
            click_change(irec['bag_others'][1])

        elif irec['bag_relic'][0] == True:
            break

    while True:
        shot.get_screen()
        break

    while True:
        shot.get_screen()
        irec.get_xy(['close','bag'])

        if irec['close'][0] == True :
            click_change(irec['close'][1])
        
        elif irec['bag'][0] == True and irec['bag'][1][0] > 500:
            break

def test():
    shot.get_screen()
    a=relic_rec()
    f=open('./modules/genshen.txt',mode='w',encoding='utf-8')
    f.write('suit,'+'seat,'+'level,'+'{:^20}'.format('main_tag')+','+'{:^20}'.format('secondary_tag')+','+'locked,'+'owner'+'\n')
    f.close()
    shot.get_screen(name='this_page.png')
    while True:
        if a.next_o():
            a.division_recognize()
            a.record()
            continue
        else:
            break