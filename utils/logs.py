# 生成日志

import os

import logging.handlers

# 文件名称
file_name = 'WEB-API.log'
# 文件目录名称
folder_path = 'systemLog'
# 文件路径


def get_file_path(file_path):
    return file_path+folder_path + '/' if folder_path in os.listdir(file_path) else get_file_path(file_path+'../')


LOG_FILE = get_file_path('./')+file_name
fmt = '%(asctime)s - %(levelname)s - %(message)s'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, backupCount=5)  # 实例化handler
logging.basicConfig(format=fmt, level=logging.DEBUG)
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
s_logger = logging.getLogger(file_name)
s_logger.addHandler(handler)
s_logger.setLevel(logging.DEBUG)


class Logger:
    @staticmethod
    def info(msg):
        s_logger.info(msg)

    @staticmethod
    def error(msg):
        s_logger.error(msg)

    @staticmethod
    def debug(msg):
        s_logger.debug(msg)

    @staticmethod
    def warning(msg):
        s_logger.warning(msg)


logger = Logger
