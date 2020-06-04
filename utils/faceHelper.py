from os.path import exists
import face_recognition
from utils.logs import logger
import db.config as db
from utils.fsHelper import FileHelper


class FacialHelper:
    success = True
    signature = []
    error = ''
    through_user = []

    def __init__(self):
        pass

    def get_signature(self, file_path,rotating=False):
        try:
            if exists(file_path):
                # 原图获取特征码
                self.signature = face_recognition.face_encodings(face_recognition.load_image_file(file_path))
                if len(self.signature) == 0:
                    logger.info('Unable to access facial information.')
                    self.signature = []
                if(rotating == True):
                    if len(self.signature) == 0:
                        # 旋转90度获取特征码
                        self.signature = face_recognition.face_encodings(face_recognition.load_image_file(FileHelper.rotary_file(file_path, 90)))
                        logger.info('Rotate 90 degrees to get face information.')
                    if len(self.signature) == 0:
                        # 旋转180度获取特征码
                        self.signature = face_recognition.face_encodings(face_recognition.load_image_file(FileHelper.rotary_file(file_path, 180)))
                        logger.info('Rotate 180 degrees to get face information.')
                    if len(self.signature) == 0:
                        # 旋转270度获取特征码
                        self.signature = face_recognition.face_encodings(face_recognition.load_image_file(FileHelper.rotary_file(file_path, 270)))
                        logger.info('Rotate 270 degrees to get face information.')
                    if len(self.signature) == 0:
                        # 旋转360度获取特征码
                        self.signature = face_recognition.face_encodings(face_recognition.load_image_file(FileHelper.rotary_file(file_path, 360)))
                        logger.info('Rotate 360 degrees to get face information.')
                    if len(self.signature) == 0:
                        logger.info('Unable to access facial information.')
                        self.signature = []
                else:
                    self.success = True
            else:
                self.success = False
                self.error = '文件不存在' + file_path
        except Exception as e:
            self.success = False
            self.error = '获取文件特征码异常.' + str(e)
        finally:
            return self

    def facial_information_comparison(self, code, user_id, session):
        try:
            through_user = []
            users = session.query(db.Facial) \
                .filter(True if user_id is True else db.Facial.UserId.in_(user_id.split(',') if type(user_id) != int else [user_id])) \
                .all()
            for u in users:
                if u.UserId not in through_user:
                    result = face_recognition.compare_faces(code, u.facial_features, 0.4)
                    for r in result:
                        if r:
                            through_user.append(u.UserId)
            self.success = True
            self.through_user = through_user
        except Exception as e:
            logger.error('Abnormal face recognition,error info is'+str(e))
            self.success = False
            self.error = '人脸信息对比异常.'
        finally:
            return self


