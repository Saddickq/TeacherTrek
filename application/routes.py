import secrets
import os
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from application import app, bcrypt, db, mail
from application.forms import (RegistrationForm, LoginForm,
                               UpdateAccountForm, RequestForm, ResetPasswordForm, RequestNewPasswordForm)
from application.models_database import User, Request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message, Mail


@app.route('/')
def welcome():
    """
    Renders the landing page template.
    :return: The rendered landing page HTML.
    """ 
    return render_template('landing_page.html')

def get_match_county():
    """
    Returns a request that matches the teacher's sub-county.
    return: The matching request or None if no match is found.
    """
    user_request = Request.query.filter_by(teacher_id=current_user.id).first()
    if user_request:
        match_request = Request.query.filter(
            (Request.destination == user_request.county) & 
            (Request.teacher_id != current_user.id) ).all()
        if match_request:
            return match_request
    return None


@app.route('/home')
def home():
    """
    Render the home page.
    Returns:
        If the user is authenticated, render the home. Html template with the match count and user request.
        If the user is not authenticated, redirect to the login page.
    """
    if current_user.is_authenticated:
        match = get_match_county()
        user_request = Request.query.filter_by(teacher_id=current_user.id).first()
        profile_pic = url_for('static', filename='images/' + current_user.image_profile)
        return render_template('home.html', title='home', image_file=profile_pic, matches=match, user_request=user_request)
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    """
    Renders the about page.
    Returns:
        The rendered HTML template of the about page.
    """ 
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    Handle user registration.
    This route renders the registration page and processes user registration submissions.
    Returns:
        If the user is already authenticated, redirects to the home page.
        If the form submission is successful, adds the user to the database, sets a flash message,
        and redirects to the login page.
        If the request is a GET or the form validation fails, renders the registration page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        username = form.username.data
        email = form.email.data
        user = User(username=username, email=email, password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Acount created successfully for {form.username.data}. Please login", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Handle user login.
    This route renders the login page and processes user login submissions.
    Returns:
        If the form submission is successful, logs in the user, sets a flash message, and
        redirects to the home page.
        If the login is unsuccessful due to an incorrect password, sets a flash message and
        renders the login page.
        If the login is unsuccessful due to an incorrect email, sets a flash message and
        renders the login page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):       
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            flash("Login Unsuccessful, Incorrect Password!", "danger")
        else:
            flash("Login Unsuccessful, Incorrect email!", "danger")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    This route logs out the user and redirects to the welcome page.
    Returns:
        Redirects to the welcome page.
    """
    logout_user()
    flash("You have loggedout successfully, see you soon", 'success')
    return redirect(url_for('welcome'))

def save_profile_picture(form_picture):
    """
    Save and resize the user's profile picture.
    Parameters:
        form_picture (FileStorage): The uploaded profile picture file.
    Returns:
        str: The file name of the saved profile picture.
    """

    random = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random + file_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pics/', picture_file_name)

    output_size = (135, 135)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_file_name

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    """
    Render and handle user account information.
    This route allows users to view and update their account information, including the option
    to change their profile picture.
    Returns:
        If the form submission is successful, updates user information and redirects to the 'account' page.
        If the request is a GET, renders the 'account.html' template with pre-filled form fields.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Check if a new profile picture is provided
        if form.picture.data:
            # Save the new profile picture and update the user's profile image
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_profile = picture_file
            
        # Update user information and commit changes to the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Set a success message and redirect to the 'account' page
        flash("Your account has been updated successfully", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Pre-fill form fields with current user information for GET requests   
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Construct the URL for the user's profile picture
    profile_pic = url_for('static', filename='images/profile_pics/' + current_user.image_profile)

    # Render the 'account.html' template with relevant context variables
    return render_template('account.html', title='Account', image_file=profile_pic, form=form)

@app.route('/request/new', methods=['POST', 'GET'])
@login_required
def create_request():
    """
    Render and handle the creation of a new teacher transfer request.
    This route allows authenticated teachers to submit a transfer request by providing details
    such as school, subjects, county, destination, and purpose.
    Returns:
        If the form submission is successful, creates a new transfer request and redirects to the 'home' page.
        If the teacher already has an existing request, displays a warning and redirects to the 'home' page.
        If the request is a GET, renders the 'create_request.html' template with the transfer request form.
    """
    form = RequestForm()
    if form.validate_on_submit():
        school = form.school.data
        subjects = form.subjects.data
        county = form.county.data
        destination = form.destination.data
        purpose = form.purpose.data
        
        existing_request = Request.query.filter_by(teacher_id=current_user.id).first()
        if existing_request:
            flash("Sorry you can only make one request at a time! kindly edit the existing request", "warning")
            return redirect(url_for('home'))
        
        request = Request(school=school, subjects=subjects, county=county,
                          destination=destination, purpose=purpose, teacher=current_user)
        with app.app_context():
            db.session.add(request)
            db.session.commit()
        flash("congrats your transfer request has been created successfully", "success")
        return redirect(url_for('home'))
    return render_template("create_request.html", title='Take Transfer', form=form, form_title='Transfer Form')


@app.route('/request/<string:request_id>', methods=['POST', 'GET'])
@login_required
def show_request(request_id):
    """
    Render the details of a transfer request.
    This route renders the details of a transfer request, including the school, subjects, county,
    destination, and purpose.
    Args:
        request_id (str): The ID of the request to display.
    Returns:
        If the request exists, renders the 'request.html' template with the request details.
        If the request does not exist, returns a 404 error.
    """
    request = Request.query.get_or_404(request_id)
    return render_template('request.html', title=request.teacher.username, request=request)


@app.route('/request/<string:request_id>/update', methods=['POST', 'GET'])
@login_required
def update_request(request_id):
    """
    Render and handle the update of a transfer request.
    This route allows authenticated teachers to update their transfer request by providing
    new details such as school, subjects, county, destination, and purpose.
    Args:
        request_id (str): The ID of the request to update.
    Returns:
        If the form submission is successful, updates the transfer request and redirects to the 'home' page.
        If the request is a GET, renders the 'create_request.html' template with the transfer request form.
    """
    req = Request.query.get_or_404(request_id)
    if req.teacher != current_user:
        abort(403)
    form = RequestForm()
    if form.validate_on_submit():
        req.school = form.school.data
        req.subjects = form.subjects.data
        req.county = form.county.data
        req.destination = form.destination.data
        req.purpose = form.purpose.data
        db.session.commit()
        flash("Your Transfer Request has been Updated Successfully", "success")
        return redirect(url_for('show_request', request_id=req.id))
    elif request.method == 'GET':
        form.school.data = req.school
        form.subjects.data = req.subjects
        form.county.data = req.county
        form.destination.data = req.destination
        form.purpose.data = req.purpose
    return render_template('create_request.html', title='Update Request', form=form, form_title='Update Request')


@app.route('/request/<string:request_id>/delete', methods=['POST'])
@login_required
def delete_request(request_id):
    """
    Delete a transfer request.
    This route allows authenticated teachers to delete their transfer request.
    Args:
        request_id (str): The ID of the request to delete.
    Returns:
        If the request is a GET, renders the 'home' page.
        If the request is a POST, deletes the transfer request and redirects to the 'home' page.
    """
    req = Request.query.get_or_404(request_id)
    if req.teacher != current_user:
        abort(403)
    db.session.delete(req)
    db.session.commit()
    flash("You have successfully deleted your made request", "success")
    return redirect(url_for('home'))

def send_email_message(user):
    """
    Sends an email message to the specified user.
    Parameters:
        user (User): The user to send the email to.
    Returns:
        None
    """
    mail = Mail(app)
    token = user.get_reset_token()
    msg_title = "Password Reset Request"
    msg = Message(msg_title, sender='teachertrek2023@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the link below: {url_for('reset_token', token=token, _external=True)}
    
If you did not request for a password reset please ignore this email
'''
    mail.send(msg)

@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestNewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email_message(user)
        flash("An email on how to reset your password has been sent", 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated successfully. Please login", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
     
