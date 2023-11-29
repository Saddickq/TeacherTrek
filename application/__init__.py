from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd2c3cbbe16934738875e619815d8922'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from application import routes
