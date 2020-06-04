# 文件处理
from utils.logs import logger
import base64
import re
import os
from PIL import Image
import uuid

UPLOAD_PATH = './uploads/'


class FileHelper:
    # 状态
    success = False
    # 文件路径
    file_path = ''
    # 错误信息
    error = '文件上传异常！'

    def __init__(self):
            pass

    def upload_base64(self, file_content, file_name):
        try:
            file_path = UPLOAD_PATH + file_name
            file = open(file_path, 'wb')
            file.write(base64.b64decode(re.sub('^data:image/\\w+;base64,', '', file_content)))
            file.close()
            self.success = True
            self.file_path = file_path
            return self
        except Exception as e:
            logger.error('Upload error, message is ' + str(e))
            self.success = False
            return self

    def upload(self, file, filename):
        try:
            file_path = UPLOAD_PATH + filename
            file.save(file_path)
            self.success = True
            self.file_path = file_path
        except Exception as e:
            logger.error('Upload error, message is ' + str(e))
            self.success = False
        finally:
            return self

    @staticmethod
    def delete(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error('文件删除异常!' + str(e))

    @staticmethod
    def rotary_file(file_path, angle):
        new_file__path = UPLOAD_PATH + str(uuid.uuid1())+'.jpg'
        Image.open(file_path).rotate(angle).save(new_file__path)
        return new_file__path





