import mysql.connector
import json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Create a connection to the database
db_connection = mysql.connector.connect(
    host=config_data['DB_HOST'],
    user=config_data['DB_USER'],
    password=config_data['DB_PASSWORD'],
    database=config_data['DB_NAME']
)

# Create a cursor to execute SQL queries
db_cursor = db_connection.cursor()

# Secret key for session management
app.secret_key = 'your_secret_key'

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
    # Example: db_cursor.execute("SELECT * FROM your_table")
    # data = db_cursor.fetchall()
    return render_template('home.html', data=data)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Execute your login SQL query here
        # Example: db_cursor.execute("SELECT * FROM user WHERE Email = %s AND Password = %s", (email, password))
        # user = db_cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials. Please try again.')

    return render_template('login.html')

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

        # Execute your registration SQL query here
        # Example: db_cursor.execute("INSERT INTO user (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
        # Commit the changes to the database
        # db_connection.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
