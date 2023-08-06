# -*- coding:utf-8 -*-
import os

import logging

from logging.handlers import TimedRotatingFileHandler



class LogController(logging.Logger):

    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    print "CURRENT_PATH:",CURRENT_PATH
    ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
    print "ROOT_PATH:",ROOT_PATH
    # LOG_PATH = os.path.join(CURRENT_PATH, 'log')
    LOG_PATH = os.path.join(ROOT_PATH, 'log')
    print "LOG_PATH:",LOG_PATH

    def __init__(self, name, level="DEBUG", stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        # file_name = os.path.join(self.LOG_PATH, '{name}.log'.format(name=self.name))
        file_name = os.path.join('.\\', '{name}.log'.format(name=self.name))
        
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):

        stream_handler = logging.StreamHandler()
        # %(levelno)s: 打印日志级别的数值
        # %(levelname)s: 打印日志级别名称
        # %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
        # %(filename)s: 打印当前执行程序名
        # %(funcName)s: 打印日志的当前函数
        # %(lineno)d: 打印日志的当前行号
        # %(asctime)s: 打印日志的时间
        # %(thread)d: 打印线程ID
        # %(threadName)s: 打印线程名称
        # %(process)d: 打印进程ID
        # %(message)s: 打印日志信息
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()


# if __name__ == '__main__':
#     log = LogController('test')
#     log.info('this is a test msg')