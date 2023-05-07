from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flaskext.mysql import MySQL

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'local.env')
load_dotenv(dotenv_path=dotenv_path)
# connect to postgres database using local.env
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DB = os.environ.get('MYSQL_DB')

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-best-buy-project'
    app.config['MYSQL_DATABASE_USER'] = MYSQL_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DATABASE_DB'] = MYSQL_DB
    app.config['MYSQL_DATABASE_HOST'] = MYSQL_HOST
    mysql.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
