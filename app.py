import mysql.connector
import json
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

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
app.secret_key = 'secret_key'

















#login works 
# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_cursor.execute("SELECT * FROM `User` WHERE `Email` = %s AND `Password` = %s", (email, password))
        user = db_cursor.fetchone()

        if user:
            # Insert into LoginLog table
            db_cursor.execute("INSERT INTO LoginLog (UserID, LoginTime) VALUES (%s, %s)", (user[0], datetime.now()))
            db_connection.commit()

            session['logged_in'] = True
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials. Please try again.')

    return render_template('login.html')

# Logout works
# Route for user logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You have been logged out.')
        return redirect(url_for('login'))
  
#  Registration works  
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        DOB = request.form['dateofbirth']

        # Execute your registration SQL query here
        try:
            db_cursor.callproc('InsertUser', (name, email, password, DOB))
            db_connection.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
            return redirect(url_for('register'))

    return render_template('register.html')



# Basic route for the home page
@app.route('/')
@login_required
def home():
    db_cursor.execute("SELECT * FROM User")
    data = db_cursor.fetchall()
    return render_template('home.html', data=data)




#INCOME

# Basic route for the income page
@app.route('/income', methods=['GET'])
@login_required
def income():
    db_cursor.execute("SELECT * FROM Income WHERE UserID = %s", (session['user_id'],))
    data = db_cursor.fetchall()
    return render_template('income.html', data=data)
    

#create income works
# Route for creating income
@app.route('/create_income', methods=['GET', 'POST'])
@login_required
def create_income():
    if request.method == 'POST':
        # Extract form data and insert into the database
        amount = request.form['amount']  # Corrected field name
        date_occurred = request.form['date_occurred']
        description = request.form['description']

        db_cursor.callproc('InsertIncome', (session['user_id'], amount, date_occurred, description))
        db_connection.commit()

        flash('Income created successfully!')
        return redirect(url_for('income'))

    return render_template('income.html')


# Route for updating income
@app.route('/update_income/<int:income_id>', methods=['GET', 'POST'])
@login_required
def update_income(income_id):
    # Fetch the existing income record from the database based on income_id
    # Replace the placeholders with your actual SQL query
    db_cursor.execute("SELECT * FROM Income WHERE income_id = %s", (income_id,))
    income = db_cursor.fetchone()

    if request.method == 'POST':
        # Extract form data and update the income record in the database
        # Replace the placeholders with your actual form fields
        amount = request.form['amount']
        date_occurred = request.form['date_occurred']
        description = request.form['description']

        # Execute your SQL query to update the income record
        # Replace the placeholders with your actual column names
        db_cursor.execute("UPDATE Income SET amount = %s, date_occurred = %s, description = %s WHERE income_id = %s",
                          (amount, date_occurred, description, income_id))
        db_connection.commit()

        flash('Income updated successfully!')
        return redirect(url_for('income'))

    return render_template('update_income.html', income=income)

# Route for deleting income
@app.route('/delete_income/<int:income_id>', methods=['GET', 'POST'])
@login_required
def delete_income(income_id):
    if request.method == 'POST':
        # Execute your SQL query to delete the income record
        # Replace the placeholders with your actual SQL query
        db_cursor.execute("DELETE FROM Income WHERE IncomeID = %s", (income_id,))
        db_connection.commit()

        flash('Income deleted successfully!')
        return redirect(url_for('income'))

    # Handle GET request (optional)
    # You may choose to render a template or provide a response for GET requests
    return render_template('income.html')





#GOAL


# Basic route for the goal page
@app.route('/goal', methods=['GET'])
@login_required
def goal():
    db_cursor.execute("SELECT * FROM Goal WHERE UserID = %s", (session['user_id'],))
    data = db_cursor.fetchall()
    return render_template('goal.html', data=data)

# Route for creating goal
@app.route('/create_goal', methods=['GET', 'POST'])
@login_required
def create_goal():
    if request.method == 'POST':
        # Extract form data and insert into the database
        target_amount = request.form['target_amount']
        current_amount = request.form['current_amount']
        deadline = request.form['deadline']
        description = request.form['description']

        # Execute your SQL query to insert the goal record
        db_cursor.execute("INSERT INTO Goal (UserID, TargetAmount, CurrentAmount, Deadline, Description) VALUES (%s, %s, %s, %s, %s)",
                          (session['user_id'], target_amount, current_amount, deadline, description))
        db_connection.commit()

        flash('Goal created successfully!')
        return redirect(url_for('goal'))

    return render_template('goal.html')

# Route for updating goal
@app.route('/update_goal/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    if request.method == 'POST':
        # Extract form data and update the database
        target_amount = request.form['target_amount']
        current_amount = request.form['current_amount']
        deadline = request.form['deadline']
        description = request.form['description']

        # Execute your SQL query to update the goal record
        db_cursor.execute("UPDATE Goal SET TargetAmount=%s, CurrentAmount=%s, Deadline=%s, Description=%s WHERE GoalID=%s",
                          (target_amount, current_amount, deadline, description, goal_id))
        db_connection.commit()

        flash('Goal updated successfully!')
        return redirect(url_for('goal'))

    # Fetch the existing goal data for pre-filling the form
    db_cursor.execute("SELECT * FROM Goal WHERE GoalID = %s", (goal_id,))
    goal_data = db_cursor.fetchone()

    return render_template('update_goal.html', goal_data=goal_data)

# Route for deleting goal
@app.route('/delete_goal/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def delete_goal(goal_id):
    if request.method == 'POST':
        # Execute your SQL query to delete the goal record
        db_cursor.execute("DELETE FROM Goal WHERE GoalID = %s", (goal_id,))
        db_connection.commit()

        flash('Goal deleted successfully!')
        return redirect(url_for('goal'))

    # Handle GET request (optional)
    # You may choose to render a template or provide a response for GET requests
    return render_template('goal.html')





#Account 

# Basic route for the account page
@app.route('/account')
@login_required
def account():
    # Fetch user data from the User table
    db_cursor.execute("SELECT * FROM User WHERE UserID = %s", (session['user_id'],))
    user_data = db_cursor.fetchall()

    # Fetch login log data from the LoginLog table
    db_cursor.execute("SELECT * FROM LoginLog WHERE UserID = %s", (session['user_id'],))
    login_log_data = db_cursor.fetchall()

    return render_template('account.html', user_data=user_data, login_log_data=login_log_data)






# Route for updating user account details
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if request.method == 'POST':
        # Extract form data and update the database
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Note: Handle password securely, consider hashing
        date_of_birth = request.form['date_of_birth']

        # Execute your SQL query to update the user record
        db_cursor.execute("UPDATE User SET Name=%s, Email=%s, Password=%s, `Date Of Birth`=%s WHERE UserID=%s",
                          (name, email, password, date_of_birth, user_id))
        db_connection.commit()

        flash('User details updated successfully!')
        return redirect(url_for('account'))

    # Fetch the existing user data for pre-filling the form
    db_cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
    user_data = db_cursor.fetchone()

    return render_template('update_user.html', user_data=user_data)

# Route for deleting user account
@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if request.method == 'POST':
        # Execute your SQL query to delete the user record
        db_cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
        db_connection.commit()

        flash('User deleted successfully!')
        return redirect(url_for('account'))

    # Fetch the existing user data for displaying it on the template
    db_cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
    user_data = db_cursor.fetchone()

    # Render the template with user data
    return render_template('account.html', user_data=user_data)






#Expenses

# Basic route for the expenses page
@app.route('/expenses')
@login_required
def expenses():
    db_cursor.execute("SELECT * FROM Expense WHERE UserID = %s", (session['user_id'],))
    data = db_cursor.fetchall()
    return render_template('expenses.html', data=data)



# Route for creating goal
@app.route('/create_expense', methods=['GET', 'POST'])
@login_required
def create_expense():
    if request.method == 'POST':
        # Extract form data and insert into the database
        amount = request.form['amount']
        date_occurred = request.form['date_occurred']
        description = request.form['description']
        expensecategory = request.form['expensecategory']

        # Execute your SQL query to insert the goal record
        db_cursor.execute("INSERT INTO Expense (UserID, Amount, DateOccurred, Description, CategoryID) VALUES (%s, %s, %s, %s, %s)",
                          (session['user_id'], amount, date_occurred, description, expensecategory))
        db_connection.commit()

        flash('Expense created successfully!')
        return redirect(url_for('expenses'))

    return render_template('expenses.html')

# Route for updating expense
@app.route('/update_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    if request.method == 'POST':
        # Extract form data and update the database
        amount = request.form['amount']
        date_occurred = request.form['date_occurred']
        description = request.form['description']
        category_type = request.form['CategoryType']

        # Execute your SQL query to update the expense record
        db_cursor.execute("UPDATE Expense SET Amount=%s, DateOccurred=%s, Description=%s, CategoryType=%s WHERE ExpenseID=%s",
                          (amount, date_occurred, description, category_type, expense_id))
        db_connection.commit()

        flash('Expense updated successfully!')
        return redirect(url_for('expenses'))

    # Fetch the existing expense data for pre-filling the form
    db_cursor.execute("SELECT * FROM Expense WHERE ExpenseID = %s", (expense_id,))
    expense_data = db_cursor.fetchone()

    return render_template('update_expense.html', expense_data=expense_data)


# Route for deleting expense
@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def delete_expense(expense_id):
    if request.method == 'POST':
        # Execute your SQL query to delete the expense record
        db_cursor.execute("DELETE FROM Expense WHERE ExpenseID = %s", (expense_id,))
        db_connection.commit()

        flash('Expense deleted successfully!')
        return redirect(url_for('expenses'))

    # Handle GET request (optional)
    # You may choose to render a template or provide a response for GET requests
    return render_template('expenses.html')





# Investments



# Basic route for the investment page
@app.route('/investment')
@login_required
def investment():
    db_cursor.execute("SELECT * FROM investment WHERE UserID = %s", (session['user_id'],))
    data = db_cursor.fetchall()
    return render_template('investment.html', data=data)


# Route for creating investment
@app.route('/create_investment', methods=['GET', 'POST'])
@login_required
def create_investment():
    if request.method == 'POST':
        # Extract form data and insert into the database
        amount = request.form['amount']
        date_occurred = request.form['date_occurred']
        description = request.form['description']
        TypeID = request.form['TypeID']

        # Execute your SQL query to insert the goal record
        db_cursor.execute("INSERT INTO Investment (UserID, Amount, DateOccurred, Description, TypeID) VALUES (%s, %s, %s, %s, %s)",
                          (session['user_id'], amount, date_occurred, description, TypeID))
        db_connection.commit()

        flash('Expense created successfully!')
        return redirect(url_for('investment'))

    return render_template('investment.html')


# Route for updating investment
@app.route('/update_investment/<int:investment_id>', methods=['GET', 'POST'])
@login_required
def update_investment(investment_id):
    if request.method == 'POST':
        # Extract form data and update the database
        amount = request.form['amount']
        date_occurred = request.form['date_occurred']
        description = request.form['description']
        type_id = request.form['TypeID']

        # Execute your SQL query to update the investment record
        db_cursor.execute("UPDATE Investment SET Amount=%s, DateOccurred=%s, Description=%s, TypeID=%s WHERE InvestmentID=%s",
                          (amount, date_occurred, description, type_id, investment_id))
        db_connection.commit()

        flash('Investment updated successfully!')
        return redirect(url_for('investments'))

    # Fetch the existing investment data for pre-filling the form
    db_cursor.execute("SELECT * FROM Investment WHERE InvestmentID = %s", (investment_id,))
    investment_data = db_cursor.fetchone()

    # Fetch investment types for dropdown
    db_cursor.execute("SELECT * FROM InvestmentType")
    investment_types = db_cursor.fetchall()

    return render_template('update_investment.html', investment_data=investment_data, investment_types=investment_types)


# Route for deleting investment
@app.route('/delete_investment/<int:investment_id>', methods=['GET', 'POST'])
@login_required
def delete_investment(investment_id):
    if request.method == 'POST':
        # Execute your SQL query to delete the investment record
        db_cursor.execute("DELETE FROM Investment WHERE InvestmentID = %s", (investment_id,))
        db_connection.commit()

        flash('Investment deleted successfully!')
        return redirect(url_for('investments'))

    # Handle GET request (optional)
    # You may choose to render a template or provide a response for GET requests
    return render_template('investments.html')





# Budget







if __name__ == '__main__':
    app.run(debug=True)
