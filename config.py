import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY  =os.environ.get('SECRET_KEY') or os.urandom(24) # Used by flask to encrypt seesion cookie
	MAIL_SUBJECT_PREFIX = 'WARRAN'
	MAIL_SENDER = 'Warran'
	ADMIN = os.environ.get('ADMIN')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	DATABASE = os.environ.get('DEV_DATABASE_URL') or \
                'sqlite:///' +os.path.join(basedir, 'data-dev.db')


class TestingConfig(Config):
	TESTING = True
	DATABASE = os.environ.get('TEST_DATABASE_URL') or \
                'sqlite:///' +os.path.join(basedir, 'data-test.db')

class ProductionConfig(Config):
	DEBUG = False
	DATABASE = os.environ.get('DATABASE_URL') or \
                'sqlite:///' +os.path.join(basedir, 'data.db')
               
config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

'''
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'warran.db')
DEBUG = False
SECRET_KEY = os.urandom(24) # Used by Flask to encrypt session cookie.
POST_PER_PAGE = 5
MAIL_HOTNAME = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USEENAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
'''
