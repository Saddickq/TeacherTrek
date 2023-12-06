from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectMultipleField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models_database import User

class RegistrationForm(FlaskForm):
    """
    User Registration Form.

    This form provides fields for a user to register, including a username, email, and password.
    The form also includes validation rules to ensure that the provided information meets certain criteria.

    Fields:
        - username (StringField): User's desired username.
        - email (StringField): User's email address.
        - password (PasswordField): User's chosen password.
        - confirm_password (PasswordField): Confirmation of the chosen password.
        - submit (SubmitField): Button to submit the registration form.

    Validators:
        - username:
            - DataRequired: Ensures that the username field is not submitted empty.
            - Length(min=3, max=20): Enforces a minimum and maximum length for the username.
        - email:
            - DataRequired: Ensures that the email field is not submitted empty.
            - Email: Validates that the email has a correct email format.
        - password:
            - DataRequired: Ensures that the password field is not submitted empty.
            - Length(min=5, max=20): Enforces a minimum and maximum length for the password.
        - confirm_password:
            - DataRequired: Ensures that the confirm_password field is not submitted empty.
            - EqualTo('password'): Validates that the confirm_password matches the password.

    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validates if a given username already exists in the database.
        Parameters:
            username (str): The username to be validated.
        Raises:
            ValidationError: If the username already exists in the database.
        Returns:
            None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This user already exist, please try a different username")

    def validate_email(self, email):
        """
        Validates if a given email already exists in the database.
        Parameters:
            email (str): The email address to be validated.
        Raises:
            ValidationError: If the email already exists in the database.
        Returns:
            None
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exist, please try a different email")


class LoginForm(FlaskForm):
    """
    User Login Form.

    This form provides fields for a user to log in, including an email, password, and an optional
    "Remember Me" checkbox for session persistence.
    The form includes validation rules to ensure that the provided information meets certain criteria.

    Fields:
        - email (StringField): User's email address.
        - password (PasswordField): User's password.
        - remember (BooleanField): Optional checkbox to remember the user's session.
        - submit (SubmitField): Button to submit the login form.

    Validators:
        - email:
            - DataRequired: Ensures that the email field is not submitted empty.
            - Email: Validates that the email has a correct email format.
        - password:
            - DataRequired: Ensures that the password field is not submitted empty.
            - Length(min=5, max=20): Enforces a minimum and maximum length for the password.

    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    User Update Account Form.

    This form provides fields for a user to update their account information, including a username,
    email, and profile picture.
    The form includes validation rules to ensure that the provided information meets certain criteria.

    Fields:
        - username (StringField): User's desired username.
        - email (StringField): User's email address.
        - picture (FileField): User's profile picture.
        - submit (SubmitField): Button to submit the update form.

    Validators:
        - username:
            - DataRequired: Ensures that the username field is not submitted empty.
            - Length(min=3, max=20): Enforces a minimum and maximum length for the username.
        - email:
            - DataRequired: Ensures that the email field is not submitted empty.
            - Email: Validates that the email has a correct email format.

    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        Validates if a given username already exists in the database.
        Parameters:
            username (str): The username to be validated.
        Raises:
            ValidationError: If the username already exists in the database.
        Returns:
            None
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This user already exist, please try a different username")

    def validate_email(self, email):
        """
        Validates if a given email already exists in the database.
        Parameters:
            email (str): The email address to be validated.
        Raises:
            ValidationError: If the email already exists in the database.
        Returns:
            None
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email already exist, please try a different email")

class RequestForm(FlaskForm):
    """
    Request Form.

    This form provides fields for a user to create a request for a transfer.
    The form includes validation rules to ensure that the provided information meets certain criteria.

    Fields:
        - school (StringField): Current school the user is transferring from.
        - subjects (StringField): Subjects the user is teaching.
        - county (SelectField): Current sub-county the user is transferring from.
        - destination (SelectField): Destination sub-county the user is transferring to.
        - purpose (TextAreaField): The reason for the transfer.
        - submit (SubmitField): Button to submit the request form.
    """
 
    sub_county = [
    'Teso South','Teso North', 'Teso Central', 'Nambale', 'Matayos', 'Butula', 'Samia', 'Bunyala'
]
    
    Subjects = ['Mathematics', 'English', 'Kiswahili', 'Biology', 'Chemistry', 'Physics', 'History and Government',
    'Geography', 'Christian Religious Education (CRE)', 'Islamic Religious Education (IRE)',
    'Hindu Religious Education (HRE)', 'Home Science', 'Art and Design', 'Agriculture', 'Computer Studies',
    'Business Studies', 'French', 'German', 'Music', 'Physical Education', 'Life Skills', 'Sign Language', 'Braile'
]

    sorted_subjects = sorted(Subjects)
    sorted_county = sorted(sub_county)

    school = StringField('Current School', validators=[DataRequired()])
    subjects = SelectField('Teaching Subjects', choices=[('', 'Choose...')] + [(subject, subject) for subject in sorted_subjects],
                           validators=[DataRequired()], render_kw={"placeholder": "Choose..."})
    county = SelectField('Current Sub-county', choices=[('', 'Choose...')] + [(sub, sub) for sub in sorted_county],
                         validators=[DataRequired()], render_kw={"placeholder": "Choose..."})
    destination = SelectField('Current Sub-county', choices=[('', 'Choose...')] + [(sub, sub) for sub in sorted_county],
                         validators=[DataRequired()], render_kw={"placeholder": "Choose..."})
    purpose = TextAreaField("What is your reason for the transfer")
    submit = SubmitField("Create Request")
     
    def validate_subjects(self, subjects):
        """
        Validates if at least one subject is selected.
        Parameters:
            subjects (list): The list of selected subjects.
        Raises:
            ValidationError: If no subject is selected.
        Returns:
            None
        """
        if not subjects:
            raise ValidationError("Please select at least one subject")
        