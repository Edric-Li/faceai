# -*- coding:utf-8 -*-
import os
from sqlalchemy import create_engine

from config.env.development import Development
from config.env.production import Production


class Config:
    env_name = ''
    env = {}

    def __init__(self):
        self.env_name = os.getenv('CURRENT_ENV')

        if self.env_name is None:
            self.env = Development()
        else:
            self.env = Production()
        try:
            Config.db_init(DB(self.env.db))
        except Exception:
            pass

    @staticmethod
    def db_init(db):
        conn = (create_engine(db.engine)).connect()
        conn.execute("commit")
        conn.execute('create'+" database "+db.name+';')
        conn.close()


class DB:
    name = ''
    engine = ''
    public_engine = ''

    def __init__(self, connection_information):
        self.name = connection_information['name']
        self.engine = connection_information['engine']
        self.public_engine = self.engine+'/'+self.name
