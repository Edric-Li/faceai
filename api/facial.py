import db.config as db
from flask import request
from utils.logs import logger
import re
from utils.fsHelper import FileHelper
from utils.faceHelper import FacialHelper
import uuid


class Facial:
    success = True
    error = ''
    session = ''
    fileHelper = FileHelper()
    facialHelper = FacialHelper()

    def __init__(self, session):
        self.session = session

    def init(self):
        self.success = True
        self.error = ''
        self.fileHelper = FileHelper()
        self.facialHelper = FacialHelper()

    def auth(self, choose):
        try:
            filename = str(uuid.uuid1())+'.jpg'

            self.init()
            parameter = request.form
            #  True 代表所有
            user_id = True
            if choose == 'base64':
                parameter = request.json

                if 'fileContent' not in parameter:
                    return {
                        'success': False,
                        'error': '缺少fileContent参数'
                    }
                if 'userId' in parameter:
                    user_id = parameter['userId']
                self.fileHelper.upload_base64(parameter['fileContent'], filename)
            else:
                if 'file' not in request.files:
                    return {
                        'success': False,
                        'error': '请使用file参数上传文件'
                    }
                if 'userId' in parameter:
                    user_id = parameter['userId']

                self.fileHelper.upload(request.files['file'], filename)
            if self.fileHelper.success:
                # 获取文件中图像的特征码
                self.facialHelper.get_signature(self.fileHelper.file_path,parameter['rotating'] if 'rotating' in parameter else False)
                if self.facialHelper.success:
                    # 特征码比对
                    self.facialHelper.facial_information_comparison(self.facialHelper.signature, user_id,
                                                                    self.session)
                    if self.facialHelper.success:
                        logger.info('Face recognition passes.userId is '+str(self.facialHelper.through_user))
                        self.success = True
                    else:
                        # 特征码比对异常
                        self.success = False
                        self.error = self.facialHelper.error
                        logger.info('facial_information_comparison error is '+self.facialHelper.error)
                else:
                    # 获取特征码异常
                    self.success = False
                    self.error = self.facialHelper.error
                    logger.info('get_signature error is ' + self.facialHelper.error)
            else:
                # 转换文件异常
                self.success = False
                self.error = '上传文件异常'
                logger.info('get_signature error is ' + self.fileHelper.error)
            through_user = self.facialHelper.through_user
            result = {
                'success': self.success,
                'through_user': through_user if (',' in str(user_id) or user_id is True)else len(through_user) > 0
            }
            if not self.success:
                result['error'] = self.error
            return result
        except Exception as e:
            logger.error('人脸识别异常,' + str(e))
            return {
                'success': False,
                'error': '人脸识别异常,' + str(e)
            }

    def registered(self):
        filename = str(uuid.uuid1())+'.jpg'
        self.init()
        if 'file' not in request.files:
            return {
                'success': False,
                'error': '请使用file参数上传文件'
            }
        if 'userId' not in request.form:
            return {
                'success': False,
                'error': '缺少userId参数'
            }
        # 文件保存
        file = request.files['file']
        self.fileHelper.upload(file, filename)
        # 获取特征码
        facial = self.facialHelper.get_signature(self.fileHelper.file_path)
        if facial.success:
            if len(facial.signature) > 0:
                return Facial.add_facial(request.form['userId'], facial.signature, self.session)
            else:
                logger.warning('未识别到有有效人脸信息!'+request.form['userId'])
                return {
                    'success': False,
                    'error': '未识别到有有效人脸信息'
                }
        else:
            return {
                'success': False,
                'error': facial.error
            }

    # 面部信息注册--base64
    def registered_base64(self):
        try:
            filename = str(uuid.uuid1()) + '.jpg'
            self.init()
            if 'fileContent' not in request.json:
                self.success = False
                self.error = '缺少fileContent参数'
                return
            if 'userId' not in request.json:
                self.success = False
                self.error = '缺少userId参数'
                return
            # 文件保存
            file_content = re.sub('^data:image/\\w+;base64,', '', request.json['fileContent'])
            self.fileHelper.upload_base64(file_content=file_content, file_name=filename)

            if self.fileHelper.success:
                # 获取特征码
                self.facialHelper.get_signature(self.fileHelper.file_path,request.json['rotating'] if 'rotating' in request.json else False)
                # 面部信息注册
                if self.facialHelper.success:
                    if len(self.facialHelper.signature) > 0:
                        return Facial.add_facial(request.json['userId'], self.facialHelper.signature, self.session)
                    else:
                        logger.warning('未识别到有有效人脸信息!')
                        self.success=False
                        self.error='未识别到有有效人脸信息'
                else:
                    self.success = False
                    self.error = self.facialHelper.error
                    return
            else:
                self.success = False
                self.error = '文件异常!'
        except Exception as e:
            logger.error('registered_base64 error is '+str(e))
            self.success = False
            self.error = '面部信息注册异常!'
        finally:
            result = {
                'success': self.success,
            }
            if not self.success:
                result['error'] = self.error

            return result

    def check_facial(self):
        if 'userId' not in request.json:
            return {
                'success': False,
                'error': 'userId不允许为空！'
            }
        return Facial.find_facial(request.json['userId'], self.session)

    @staticmethod
    def add_facial(user_id, signature, session):
        try:
            new_facial = db.Facial(UserId=user_id, facial_features=signature[0])
            session.add(new_facial)
            session.commit()
            logger.info('Add facial features.(user_id is ' + str(user_id) + ')')
            return {
                'success': True
            }
        except Exception as e:
            logger.error('add_facial error is ' + str(e))
        return {
            'success': False
        }

    @staticmethod
    def find_facial(user_id, session):
        try:
            count = session.query(db.Facial).filter(db.Facial.UserId == user_id).count()
            if(count>0):
                return {
                    'success': True,
                }
            else:
                return {
                    'success': False
                }

            pass
        except Exception as e:
            logger.error('验证面部信息异常。'+str(e))
            return {
                'success': False,
                'error': '验证面部信息异常。'+str(e)
            }

