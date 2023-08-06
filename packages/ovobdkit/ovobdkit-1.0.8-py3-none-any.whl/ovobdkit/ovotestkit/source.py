import os

class BaseSource:
    pass

class DbSource:
    def __init__(self, 
                    db_type=os.getenv('DB_TYPE'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT'),
                    schema=os.getenv('DB_SCHEMA'),
                    login=os.getenv('DB_LOGIN'), 
                    pwd=os.getenv('DB_PASSWORD')):
        '''
            define database source. 
                defaultly taking following values from 
        '''
        pass

class FileSource:
    def __init__(self):
        pass