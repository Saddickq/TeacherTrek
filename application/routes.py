import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from application import app, bcrypt, db
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm
from application.models_database import User, Requests
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def welcome():
    return render_template('landing_page.html', title='welcome')

@app.route('/home')
def home():
    return render_template('home.html', title='home')

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
    form_picture.save(picture_path)
    
    print(f'Filename: {form_picture.filename}')
    print(f'Extension: {file_ext}')
    
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
