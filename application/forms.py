from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models_database import User

class RegistrationForm(FlaskForm):
    " User Registraton form"
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This user already exist, please try a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exist, please try a different email")


class LoginForm(FlaskForm):
    " User Login form"
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ User update account form """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This user already exist, please try a different username")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email already exist, please try a different email")

class RequestForm(FlaskForm):
    sub_county = [('Teso South', 'Teso South'), ('Teso North', 'Teso North'),
                  ('Teso Central', 'Teso Central'), ('Nambale', 'Nambale'), ('Budalangi', 'Budalangi')]
    
    school = StringField('Current School', validators=[DataRequired()])
    subjects = StringField('Teaching Subjects', validators=[DataRequired()])
    county = SelectField('Current Sub-county', choices=sub_county, validators=[DataRequired()])
    destination = SelectField('Destination Sub-county', choices=sub_county, validators=[DataRequired()])
    purpose = TextAreaField("What is your reason for the transfer")
    submit = SubmitField("Create Request")
 