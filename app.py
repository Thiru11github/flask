from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USERNAME')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))  # Default to 3306 if not set

mysql = MySQL(app)

# Route for Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Database query for authentication
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['logged_in'] = True
            session['email'] = user[1]  # Assuming email is the second field
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard if login successful
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('index.html')

# Route for the Dashboard page (requires login)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f"Welcome to your dashboard, {session['email']}!"
    else:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
