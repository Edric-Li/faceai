from sqlalchemy import Column, PickleType,Integer
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()


class Facial(base):

    __tablename__ = 'facial'

    id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer)
    facial_features = Column(PickleType)

    def __str__(self):
        return self.id

    @staticmethod
    def create_table(connection):
        base.metadata.create_all(connection)


