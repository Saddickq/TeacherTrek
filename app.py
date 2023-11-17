from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '7fc93b5b9790'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/register')
def login():
    return render_template('register.html', title='register')

if __name__ == "__main__":
    app.run(debug=True)
