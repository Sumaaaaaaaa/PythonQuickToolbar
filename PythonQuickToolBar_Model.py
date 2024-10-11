import logging
from concurrent.futures import ThreadPoolExecutor

# Logging 的基本设置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 模型层部分
class PythonQuickToolBar_Model:
    # 实例化 = 创建对象池
    def __init__(self) -> None:
        self.__threading_init()
    
    # 删除 = 释放对象池
    def __del__(self) -> None:
        self.__threading_close()
    
    # 上交一个任务
    def threading_submit(self,fucntion):
        self.executor.submit(function)
    # 创建对象池
    def __threading_init(self):
        self.executor = ThreadPoolExecutor(max_workers=None)
        logging.debug("Thread pool has been opened.")
    # 释放对象池
    def __threading_close(self):
        self.executor.shutdown(wait=False,cancel_futures=False)
        logging.debug("Thread pool has been closed.")
    
    

# 测试

a = PythonQuickToolBar_Model()
del a
