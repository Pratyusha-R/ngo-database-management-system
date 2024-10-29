from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Hardcoded admin credentials for demonstration purposes
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'database': 'ngo_db'  # Replace with your database name
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/donors', methods=['GET', 'POST'])
def donors():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Get donor details from the form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        # Insert new donor into the database
        cursor.execute('INSERT INTO donors (name, email, phone, address) VALUES (%s, %s, %s, %s)', 
                       (name, email, phone, address))
        conn.commit()
        flash('Donor added successfully!')
        return redirect(url_for('donors'))
    
    # Fetch all donors
    cursor.execute('SELECT * FROM donors')
    donors = cursor.fetchall()
    conn.close()
    
    return render_template('donors.html', donors=donors)

@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Get volunteer details from the form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        # Insert new volunteer into the database
        cursor.execute('INSERT INTO volunteers (name, email, phone, address) VALUES (%s, %s, %s, %s)', 
                       (name, email, phone, address))
        conn.commit()
        flash('Volunteer added successfully!')
        return redirect(url_for('volunteers'))
    
    # Fetch all volunteers
    cursor.execute('SELECT * FROM volunteers')
    volunteers = cursor.fetchall()
    conn.close()
    
    return render_template('volunteers.html', volunteers=volunteers)

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Get project details from the form
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']
        
        # Insert new project into the database
        cursor.execute('INSERT INTO projects (title, description, budget) VALUES (%s, %s, %s)', 
                       (title, description, budget))
        conn.commit()
        flash('Project added successfully!')
        return redirect(url_for('projects'))
    
    # Fetch all projects
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    conn.close()
    
    return render_template('projects.html', projects=projects)

@app.route('/donations', methods=['GET', 'POST'])
def donations():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        donor_id = request.form['donor_id']
        project_id = request.form['project_id']
        amount = request.form['amount']

        # Insert new donation into the database
        cursor.execute('INSERT INTO donations (donor_id, project_id, amount) VALUES (%s, %s, %s)', 
                       (donor_id, project_id, amount))
        conn.commit()
        flash('Donation added successfully!')
        return redirect(url_for('donations'))
    
    # Fetch all donations
    cursor.execute('SELECT donations.id, donors.name, projects.title, donations.amount FROM donations '
                   'JOIN donors ON donations.donor_id = donors.id '
                   'JOIN projects ON donations.project_id = projects.id')
    donations = cursor.fetchall()
    conn.close()
    
    return render_template('donations.html', donations=donations)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
