from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flaskext.mysql import MySQL

# connect to postgres database using local.env
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
MYSQL_DB = os.environ.get('MYSQL_DB')

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ark-biotech-take-home-project'
    app.config['MYSQL_DATABASE_USER'] = 'com303wwang4'
    app.config['MYSQL_DATABASE_PASSWORD'] = "ww8735ww"
    app.config['MYSQL_DATABASE_DB'] = 'com303fpcw'
    app.config['MYSQL_DATABASE_HOST'] = '136.244.224.221'
    mysql.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
