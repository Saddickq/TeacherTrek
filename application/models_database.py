from application import db, login_manager
from uuid import uuid4
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid4()), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_profile = db.Column(db.String(20), nullable=False, default='kids.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f'<User {self.username} Email {self.email}>'

class Requests(db.Model):
    id = db.Column(db.String(25), primary_key=True, nullable=False, default=str(uuid4()))
    request_made_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    purpose = db.Column(db.Text, nullable=True)
    
    def __str__(self):
        """ String method """
        return f'<Request made on {self.request_made_on}>'
