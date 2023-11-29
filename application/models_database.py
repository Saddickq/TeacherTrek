from application import db, login_manager
from uuid import uuid4
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    requests = db.relationship('Request', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<User {self.username} Email {self.email}>'

class Request(db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    request_made_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    school = db.Column(db.String(30), nullable=False)
    subjects = db.Column(db.String(30), nullable=False)
    county = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    purpose = db.Column(db.Text(), nullable=True)
    teacher_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        dictionary = {}
        for key, value in self.__dict__.items():
            dictionary[key] = str(value)
        dictionary.pop('_sa_instance_state')
        return dictionary
            
    def __str__(self):
        """ String method """
        return f'Request made on {self.request_made_on}'
