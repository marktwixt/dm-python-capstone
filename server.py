from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import User, Project, Task, Equipment, db, login_manager, app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Register a new user
        pass
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Log in a user
        pass
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
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
