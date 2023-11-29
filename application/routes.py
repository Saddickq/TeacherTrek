import secrets
import os
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, session
from application import app, bcrypt, db
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestForm
from application.models_database import User, Request
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def welcome():
    return render_template('landing_page.html', title='welcome')

def get_match_county():
    user_request = Request.query.filter_by(teacher_id=current_user.id).first()
    if user_request:
        match_request = Request.query.filter_by(destination=user_request.destination).first()
        if match_request:
            return match_request
    return None

@app.route('/home')
def home():
    # match = get_match_county()
    user_request = Request.query.filter_by(teacher_id=current_user.id).first()
    return render_template('home.html', title='home', user_request=user_request)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        is_password = bcrypt.check_password_hash(user.password, form.password.data)
        if user and is_password:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful, Please check email and password!", "danger")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    """ Log user out """
    logout_user()
    flash("You have loggedout successfully, see you soon", 'success')
    return redirect(url_for('welcome'))

def save_profile_picture(form_picture):
    random = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random + file_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_file_name)

    output_size = (135, 135)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_file_name

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_profile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated successfully", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='images/' + current_user.image_profile)
    return render_template('account.html', title='Account', image_file=profile_pic, form=form)

@app.route('/request/new', methods=['POST', 'GET'])
@login_required
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        school = form.school.data
        subjects = form.subjects.data
        county = form.county.data
        destination = form.destination.data
        purpose = form.purpose.data
        request = Request(school=school, subjects=subjects, county=county,
                          destination=destination, purpose=purpose, teacher=current_user)
        with app.app_context():
            db.session.add(request)
            db.session.commit()
        flash("congrats your transfer have been requested for", "success")
        return redirect(url_for('home'))
    return render_template("create_request.html", title='Take Transfer', form=form)