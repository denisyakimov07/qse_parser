import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)


class _Environment:

    def __init__(self):

        '''DB_PASSWORD'''
        self.DB_DATABASE_TYPE = os.getenv('DB_DATABASE_TYPE')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_DATABASE = os.getenv('DB_DATABASE')
        self.DB_DATABASE_TYPE = os.getenv('DB_DATABASE_TYPE')
        self.DB_PORT = os.getenv('DB_PORT')

        '''API_PASSWORD'''
        self.ACU_USER_ID = os.getenv('ACU_USER_ID')
        self.ACU_API_KEY = os.getenv('ACU_API_KEY')

        self.DEBUG_STATUS = os.getenv('DEBUG_STATUS')
        self.SECRET_KEY = os.getenv('SECRET_KEY')


        '''API_PASSWORD'''
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')


        """GMAIL"""
        self.MAIL_SERVER = os.getenv('MAIL_SERVER')
        self.MAIL_PORT = os.getenv('MAIL_PORT')
        self.MAIL_USE_SSL = True
        self.MAIL_USE_TLS = False
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

        self.SCHEDULER_KEY = os.getenv('SCHEDULER_KEY')


__environment = _Environment()


def get_env():
    return __environment
