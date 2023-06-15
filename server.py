from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Project, Task, Equipment, db, login_manager, app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/projects')
@login_required
def view_projects():
    # Get all projects from the database
    pass

@app.route('/projects/<int:project_id>', methods=['GET', 'POST'])
@login_required
def view_project(project_id):
    if request.method == 'POST':
        # Update a project
        pass
     # Get a specific project from the database
    pass

@app.route('/tasks')
@login_required
def view_tasks():
    # Get all tasks from the database
    pass

@app.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
@login_required
def view_task(task_id):
    if request.method == 'POST':
        # Update a task
        pass
    # Get a specific task from the database
    pass

@app.route('/equipment')
@login_required
def view_equipment():
    # Get all equipment from the database
    pass

@app.route('/equipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def view_single_equipment(equipment_id):
    if request.method == 'POST':
        # Update an equipment
        pass
    # Get a specific equipment from the database
    pass


if __name__ == '__main__':
    app.run(debug=True)
