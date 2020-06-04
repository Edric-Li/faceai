# 路由配置

from api.facial import Facial
import db.config as db


class GETRouter:

    def __init__(self):
        pass

    @staticmethod
    def redirect(url):
        if url == "welcome":
            return str('Hello,lynceus!')

        if url == "healthcheck":
            return {'success':True}

        else:
            return str('The requested resource does not exist. ' + url)


class PostRouter:

    def __init__(self):
        pass

    @staticmethod
    def redirect(url):

        session = db.DBSession()

        r = str('The requested resource does not exist. ' + url)

        if url == 'registered':
            r = Facial(session).registered()

        if url == 'registered_base64':
            r = Facial(session).registered_base64()

        if url == 'auth':
            r = Facial(session).auth(choose='upload')

        if url == 'auth_base64':
            r = Facial(session).auth(choose='base64')

        if url == 'check_facial':
            r = Facial(session).check_facial()

        session.close()
        return r
