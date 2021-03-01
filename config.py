import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
#basedir = os.getcwd()

#load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(os.path.join(basedir, 'secret/.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#print('dir =')
#print(dir())
#print()
#print('vars =')
#print(vars())
#print()
#print('globals =')
#print(globals())
#print()
#print('locals =')
#print(locals())
