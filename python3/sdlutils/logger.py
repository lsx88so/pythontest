#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging
from logging import handlers

class Logger():
    #日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL
    }

    def __init__(self,filename=None,logname=None,logmode=1,level='info',interval=1,when='midnight',backCount=3,datefmt=None,fmt=r'%(asctime)s - [Thread id : %(thread)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger()
        if logname:
            self.logger = logging.getLogger(logname)
        if not filename:
            logmode = 1
        #设置日志格式
        format_str = logging.Formatter(fmt)
        if datefmt:
            format_str = logging.Formatter(fmt, datefmt)
        #设置日志级别
        self.logger.setLevel(self.level_relations.get(level, logging.INFO))
       
        if logmode != 1:
            #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            #往文件里写入
            #指定间隔时间自动生成文件的处理器
            th = handlers.TimedRotatingFileHandler(filename=filename,interval=interval,when=when,backupCount=backCount,encoding='utf-8')
            #设置文件里写入的格式
            th.setFormatter(format_str)
            self.logger.addHandler(th)
        if logmode != 2:
            #往屏幕上输出
            sh = logging.StreamHandler()
            #设置屏幕上显示的格式
            sh.setFormatter(format_str)
            #把对象加到logger里，可以输出到屏幕
            self.logger.addHandler(sh)

    def setLogLevel(self, loglevel):
        self.logger.setLevel(self.level_relations.get(loglevel, logging.INFO))

'''
日志可输出格式：
asctime	        %(asctime)s	        将日志的时间构造成可读的形式，默认情况下是‘2016-02-08 12:00:00,123’精确到毫秒
name	        %(name)s	        所使用的日志器名称，默认是'root'，因为默认使用的是 rootLogger
filename	    %(filename)s	    调用日志输出函数的模块的文件名； pathname的文件名部分，包含文件后缀
funcName	    %(funcName)s	    由哪个function发出的log， 调用日志输出函数的函数名
levelname	    %(levelname)s	    日志的最终等级（被filter修改后的）
message	        %(message)s	        日志信息， 日志记录的文本内容
lineno	        %(lineno)d	        当前日志的行号， 调用日志输出函数的语句所在的代码行
levelno	        %(levelno)s	        该日志记录的数字形式的日志级别（10, 20, 30, 40, 50）
pathname	    %(pathname)s	    完整路径 ，调用日志输出函数的模块的完整路径名，可能没有
process	        %(process)s	        当前进程， 进程ID。可能没有
processName	    %(processName)s	    进程名称，Python 3.1新增
thread	        %(thread)s	        当前线程， 线程ID。可能没有
threadName	    %(thread)s	        线程名称
module	        %(module)s	        调用日志输出函数的模块名， filename的名称部分，不包含后缀即不包含文件后缀的文件名
created	        %(created)f	        当前时间，用UNIX标准的表示时间的浮点数表示； 日志事件发生的时间--时间戳，就是当时调用time.time()函数返回的值
relativeCreated	%(relativeCreated)d	输出日志信息时的，自Logger创建以 来的毫秒数； 日志事件发生的时间相对于logging模块加载时间的相对毫秒数
msecs	        %(msecs)d	        日志事件发生事件的毫秒部分。logging.basicConfig()中用了参数datefmt，将会去掉asctime中产生的毫秒部分，可以用这个加上
'''
'''
时间格式：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00-59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
'''

#使用方式
#log = Logger('all.log',level='debug')
#log.logger.debug('debug')
#log.logger.info('info')
#log.logger.warning('警告')
#log.logger.error('报错')
#log.logger.critical('严重')
#Logger('error.log', level='error').logger.error('error')