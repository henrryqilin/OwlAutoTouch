import time

def second_transform(Time):
    if Time < 1 and Time > 0.001:
        return '{0:.1f}ms'.format(Time*1000)
    elif Time <= 0.001:
        return '{0:.3f}ms'.format(Time*1000)
    elif Time >= 1:
        return '{0:.1f}s'.format(Time)

def timer(func):
    """
    计时器装饰器
    """
    def get_time(*args, **kwargs):
        start_time=time.time()
        res=func(*args, **kwargs)
        use_time=time.time()-start_time
        print('Function {0} use time:{1}'.format(func.__name__,second_transform(use_time)))
        return res
    
    return get_time

def average_timer(t = 10):
    """
    多次运行取平均值
    """
    def timer(func):
        def get_time(*args, **kwargs):
            total = 0

            for i in range(t):
                start_time=time.time()
                res=func(*args, **kwargs)
                use_time=time.time()-start_time
                total += use_time
                print('Function {0} use time:{1}'.format(func.__name__,second_transform(use_time)))
            
            print('Function {0} run for {1} times,average time consumption:{2}\n'\
                  .format(func.__name__,t,second_transform(total / t)))
            return res
        return get_time
    return timer

if __name__ == '__main__':
    @timer
    def wast_time(Sleep_Time):
        time.sleep(Sleep_Time)
        return
    
    wast_time(0.01)