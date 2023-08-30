from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='../templates',static_folder='../static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kodland.db'  # SQLite veritabanı bağlantısı

db = SQLAlchemy(app)