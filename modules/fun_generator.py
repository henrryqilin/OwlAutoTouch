# speed for generator is not necessary
# because it run only once

def dict_output(Key_List,Value_List):
    if len(Key_List) != len(Value_List):
        print('不是哥们,你这左右腿不一般长我咋整啊.')
        assert 9 > 10

    with open('output.txt','w',encoding='utf-8') as f:
        f.write('{')
        for i in range(len(Key_List)):
            f.write('\"{0}\":\'{1}\','.format(Key_List[i],Value_List[i]))

        f.seek(f.tell() - 1)
        f.write('}')
    return

def list_output(List):
    with open('output.txt','w',encoding='utf-8') as f:
        f.write('[')
        for i in range(len(List)):
            f.write('\'{0}\','.format(List[i]))

        f.seek(f.tell() - 1)
        f.write(']')
    return

def ganzhi_conjugate(Lista,Listb,Mode = 'merge',Path = 'output.txt'):
    """
        Mode = 'merge','part','output'
    """
    len_a,len_b = len(Lista),len(Listb)
    
    count_process = [len_a,len_b]
    while True:
        if count_process[0] % count_process[1] != 0:
            c = count_process[0]
            count_process[0] = count_process[1]
            count_process[1] = c % count_process[0]
        else:
            hcf = count_process[1]
            break
    
    lcm = int(len_a * len_b / hcf)

    list1 = []
    list2 = []
    for i in range(int(lcm / len_a)):
        for line in Lista:
            list1.append(line)

    for i in range(int(lcm / len_b)):
        for line in Listb:
            list2.append(line)
    
    if Mode == 'merge':
        res = []
        for i in range(lcm):
            res.append(str(list1[i]) + str(list2[i]))
        return res
        
    elif Mode == 'part':
        return list1,list2
    
    elif Mode == 'output':
        with open(f'{Path}','w',encoding = 'utf-8') as f:
                    f.write('[')
                    for i in range(lcm):
                        f.write('\'{0}{1}\','.format(list1[i],list2[i]))

                    f.seek(f.tell() - 1)
                    f.write(']')

def list_repet_generator(Repet_List,Times):
    """
        [1,2,3,1,2,3]
    """
    res = []
    for line in range(Times):
        for i in Repet_List:
            res.append(i)
    
    return res

def repet_element_generator(Repet_List,Times):
    """
        [1,1,1,2,2,2,3,3,3]
    """
    res = []
    for i in Repet_List:
        for line in range(Times):
            res.append(i)
    
    return res

def file2py(File_Name,Encoding = 'utf-8'):
    with open(File_Name,mode = 'r',encoding = Encoding) as f:
        return eval(f.read())


if __name__ == '__main__':
    # dict_output(list(range(1,13)),list('木木土火火土金金土水水土'))
    # dict_output(ganzhi_conjugate(list('甲乙丙丁戊己庚辛壬癸'),list('子丑寅某辰巳无为申酉戌亥')),\
    #             repet_element_generator(list('戊己庚辛壬癸'),10))
    # dict_output(list({'蓬':(2, 1),'任':(2,0),'冲':(1, 0),'辅':(0, 0),'英':(0, 1),'芮':(0, 2),'柱':(1, 2),'心':(2, 2),'禽':(1,1)}.values()),list('蓬任冲辅英芮柱心禽'))
    # dict_output(list({1:(2,1),2:(0,2),3:(1,0),4:(0,0),5:(1,1),6:(2,2),7:(1,2),8:(2,0),9:(0,1)}.values()),
    #             list({1:(2,1),2:(0,2),3:(1,0),4:(0,0),5:(1,1),6:(2,2),7:(1,2),8:(2,0),9:(0,1)}.keys()))
    dict_output(list('蓬任冲辅英芮柱心禽'),list('水土木木火土金金土'))