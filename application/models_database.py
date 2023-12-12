from application import db, login_manager, app
from uuid import uuid4
from itsdangerous import TimedJSONWebSignatureSerializer as Serialiser
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """
    Load user from the database based on the provided user_id
    Parameters:
        user_id: id of the user to load
    Returns:
        The loaded User object
    """
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """
    Model representing a user in the database and inheriting from the UserMixin and db.Model
    Attributes:
        id(str): The id of the user
        username(str): The username of the user
        email(str): The email of the user
        image_profile(str): The filename of the profile picture of the user
        password(str): The hashed password of the user
        requests(Relationship): The requests made by the user

        Methods:
        __repr__(): String representation of the User object.
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    requests = db.relationship('Request', backref='teacher', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        """
        Generate a reset token for the current user.
        Parameters:
            expires_sec (int): The number of seconds until the reset token expires. Default is 1800 seconds.
        Returns:
            str: The reset token as a string.
        """
        s = Serialiser(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        """
        Verify a token and return the corresponding user.
        Parameters:
            token (str): The token to be verified.
        Returns:
            User or None: The corresponding user if the token is valid, or None if the token is invalid.
        """
        s = Serialiser(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        

    def __repr__(self):
        """ 
        String method 
        Returns:
            The string representation of the User object
        """
        return f'<User {self.username} Email {self.email}>'

class Request(db.Model):
    """
        Represents a request made by a teacher.

        Attributes:
            id (str): The unique identifier of the request.
            request_made_on (DateTime): The date and time when the request was made.
            school (str): The name of the current school where the teacher is stationed.
            subjects (str): The subjects taught by the teacher.
            county (str): The current county where the teacher is stationed.
            destination (str): The destination county where the teacher intends to transfer.
            purpose (str): The purpose of the request.
            teacher_id (str): The ID of the teacher who made the request.
        
        Methods:
            to_dict(): Converts the object to a dictionary representation.
            __str__(): String representation of the Request object.
    """
    id = db.Column(db.String(36), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    request_made_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    school = db.Column(db.String(30), nullable=False)
    subjects = db.Column(db.String(30), nullable=False)
    county = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    purpose = db.Column(db.Text(), nullable=True)
    teacher_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        """
        Converts the object to a dictionary representation.
        Returns:
            dictionary (dict): A dictionary representation of the object,
            where each key is an attribute name and each value is the string
            representation of the attribute value.
        """
        dictionary = {}
        for key, value in self.__dict__.items():
            dictionary[key] = str(value)
        dictionary.pop('_sa_instance_state')
        return dictionary
            
    def __str__(self):
        """ 
        String method 
        Returns:
            The string representation of the Request object
        """
        return f'Request made on {self.request_made_on}'
