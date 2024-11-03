import os,time,logging

from rich.logging import RichHandler

class Logger():
    
    def __init__(self,Config_Input):
        self.DIR = os.path.join(Config_Input['dir'],'logs')
        self.config = Config_Input['config']
        
        self.files_arrange()
        self.log = self.logger_init()
        return
    
    def files_arrange(self):
        file_list = os.listdir(self.DIR)
        log_list = []

        for i in file_list:
            if 'log_' in i and '.txt' in i:
                log_list.append(i)
        
        log_list.sort()

        while len(log_list) > self.config['basic']["log_quantity"]:
            os.remove(os.path.join(self.DIR,log_list.pop(0)))
        
        return
    
    def logger_init(self):
        console_handler = RichHandler(show_level = False,show_time = False)# 创建一个 RichHandler 用于将日志输出到控制台
        file_handler = logging.FileHandler('{0}'.format(os.path.join(self.DIR,'log_{name}_{time}.txt'\
                                           .format(name = self.config['basic']["name"],time = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime()))))\
                                           ,mode = 'w',encoding = 'utf-8')# 创建一个文件处理器，将日志输出到文件
        logging.basicConfig(
            level="NOTSET",  # 日志级别
            format= '%(levelname)s %(asctime)s │%(message)s',  
            datefmt="%H:%M:%S",  # 时间格式
            handlers=(console_handler,file_handler)  
        )
        logger = logging.getLogger("{0}_logger".format(self.config['basic']['name']))# 创建一个日志记录器   

        return logger

    def log_test(self):
        self.log.info("这是一条信息日志")
        self.log.warning("这是一条警告日志")
        self.log.error("这是一条错误日志")
        return

    def info(self,Message):
        self.log.info(Message)
        return

    def warning(self,Message):
        self.log.warning(Message)
        return

    def error(self,Message):
        self.log.error(Message)
        return
