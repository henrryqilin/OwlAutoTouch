import time,os
from modules.basic import adb_test,screen_shot

a=screen_shot()
adb_test()

def screenshot(mode=0,sleep=3,shot_name=''):
	"""
	mode:int类型,0为截图命名为时间,1为截图命名为screenshot+数字,2为不加任何参数的截图
	sleep:int类型,
	name:str类型,保存的文件名,如果存在且不为空字符串则以该参数命名截图
	return:None
	"""
	if mode == 0 and shot_name == '':   
		time_now = time.strftime("%Y-%m-%d %H.%M.%S",time.localtime())
		a.get_screen(save_path='./imgs/develop/',name=f'{time_now}.png')

	elif mode == 1 and shot_name == '':
		img_list = os.listdir(path='./imgs/develop')
		copy_list=img_list.copy()

		for i in img_list:
			if 'screenshot' in i:
				copy_list.remove(i)
		number = len(img_list)-len(copy_list)
		a.get_screen(save_path='./imgs/develop/',name='screenshot{:0>3}.png'.format(number))

	elif mode == 2:
		a.get_screen()

	elif shot_name != '':
		a.get_screen(save_path= f'./imgs/develop/',name=f'{shot_name}.png')
	print('完成！')
	time.sleep(sleep)
	return

print('开始！')
time.sleep(1)
while True:
    screenshot(2)
    time.sleep(1)