# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.Facial import Facial
from config.index import Config, DB

engine = create_engine(DB(Config().env.db).public_engine)

DBSession = sessionmaker(bind=engine)

try:
    connection = engine.connect()

    Facial.create_table(connection)

    connection.close()

except Exception as e:
    print('Create table exception.'+str(e))
