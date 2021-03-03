from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
#import python_dotenv

from flask_moment import Moment

app = Flask(__name__, static_url_path='') #, static_folder='web/static')
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
moment = Moment(app)
database_url = os.environ.get('DATABASE_URL')
print(f'{database_url}\\{Config.SQLALCHEMY_DATABASE_URI}')

from web import routes, models

