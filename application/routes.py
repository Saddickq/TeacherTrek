from flask import render_template, redirect, url_for, flash
from application import app, bcrypt, db
from application.forms import RegistrationForm, LoginForm
from application.models_database import User, Requests
from flask_login import login_user, current_user, logout_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


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
            flash("You have logged in successfully", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful, Please check email and password!", "danger")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    """ Log user out """
    logout_user()
    flash("You have loggedout successfully, see you soon", 'success')
    return redirect(url_for('login'))


@app.route('/account')
def account():
    return render_template('account.html', title='Account')
