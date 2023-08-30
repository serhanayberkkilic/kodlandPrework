from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__, template_folder='../templates',static_folder='../static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kodland.db'  # SQLite veritabanı bağlantısı
app.secret_key = 'kodland'  # Session güvenliği için gerekli

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'