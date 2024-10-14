import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from enum import Enum, auto

# Logging 的基本设置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# 表明任务的状态
class ProcessingState(Enum):
    IN_PROGRESS = auto()
    FAILED = auto()
    SUCCESS = auto()


# 模型层部分
class PythonQuickToolBar_Model:

    # 实例化 = 创建对象池、空任务列
    def __init__(self) -> None:
        self.__threading_init()
        self.__resultQueue = queue.Queue()

    # 删除 = 释放对象池
    def __del__(self) -> None:
        self.__threading_close()

    # 上交一个任务
    def threading_submit(self, func):

        # 如果是非可执行的方法
        if not callable(func):
            raise ValueError(f"输入的'{func}'，并非一个可执行对象。")

        # 构建实际执行方法
        def function():
            try:
                # 执行方法
                executionResult = func()
            except Exception as e:
                # 出错的情况
                self.__resultQueue.put(item=(ProcessingState.FAILED, e))
                raise
            else:
                # 成功运行
                self.__resultQueue.put(item=(ProcessingState.SUCCESS, executionResult))

        self.executor.submit(function)

    # 获取一个最新的运行结果，
    def popResult(self):
        if not self.__resultQueue.empty():
            return self.__resultQueue.get()
        return None

    def __len__(self):
        return len(self.__resultQueue)

    # 创建对象池
    def __threading_init(self):
        self.executor = ThreadPoolExecutor(max_workers=None)
        logging.debug("Thread pool has been opened.")

    # 释放对象池
    def __threading_close(self):
        self.executor.shutdown(wait=False, cancel_futures=False)
        logging.debug("Thread pool has been closed.")

