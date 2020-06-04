# Production 环境
import os


class Production:
    db = {}

    def __init__(self):
        if os.getenv('MYSQL_DATABASE') is not None:

            self.db = {
                    'name': os.getenv('MYSQL_DATABASE'),
                    'engine': 'mysql+mysqlconnector://'+os.getenv('MYSQL_USER')+':'+os.getenv('MYSQL_PASSWORD')+'@'+os.getenv('MYSQL_ADDR')
               }





