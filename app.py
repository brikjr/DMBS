import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Change this configuration according to your MySQL setup
app.config['SQLALCHEMY_DATABASE_URI'] = config_data['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Define your User model
class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)

# Check if the user is logged in for each route that requires authentication
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# Basic route for the home page
@app.route('/')
@login_required
def home():
    return render_template('home.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(Email=email, Password=password).first()

        if user:
            session['logged_in'] = True
            session['user_id'] = user.UserID
            session['user_name'] = user.Name
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials. Please try again.')

    return render_template('login.html')

# Route for user logout
# Route for user logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You have been logged out.')
        return redirect(url_for('login'))


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email is already in use
        existing_user = User.query.filter_by(Email=email).first()
        if existing_user:
            flash('Email is already in use. Please choose another one.')
        else:
            # Create a new user
            new_user = User(Name=name, Email=email, Password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
