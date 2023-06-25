import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Project, Task, Equipment, TrailSystem, ExpenseReport, db
from app import login_manager, app
from forms import ProjectForm, TaskForm, TrailSystemForm, ExpenseReportForm
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import datetime
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

# --- Registration/Login/Logout ---

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

# --- Equipment ---

@app.route('/equipment', methods=['GET', 'POST'])
@login_required
def equipment():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        maintenance_schedule = request.form['maintenance_schedule']

        new_equipment = Equipment(name=name, description=description, status=status, maintenance_schedule=maintenance_schedule)
        db.session.add(new_equipment)
        db.session.commit()

        flash('Equipment added successfully.', 'success')
        return redirect(url_for('equipment'))

    equipment = Equipment.query.all()
    return render_template('equipment.html', equipment=equipment)

@app.route('/equipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def single_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)

    if request.method == 'POST':
        equipment.name = request.form['name']
        equipment.description = request.form['description']
        equipment.status = request.form['status']
        equipment.maintenance_schedule = request.form['maintenance_schedule']

        db.session.commit()
        flash('Equipment updated successfully.', 'success')
        return redirect(url_for('equipment'))

    return render_template('edit_equipment.html', equipment=equipment)

@app.route('/equipment/<int:equipment_id>/delete', methods=['POST'])
@login_required
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)

    db.session.delete(equipment)
    db.session.commit()

    flash('Equipment deleted successfully.', 'success')
    return redirect(url_for('equipment'))

# --- Projects ---

@app.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']

        new_project = Project(name=name, description=description, status=status, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()

        flash('Project added successfully.', 'success')
        return redirect(url_for('projects'))

    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=projects)

@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()

    if form.validate_on_submit():
        new_project = Project(name=form.name.data, description=form.description.data, status=form.status.data, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()

        flash('Project added successfully.', 'success')
        return redirect(url_for('projects'))

    return render_template('new_project.html', form=form)

@app.route('/projects/<int:project_id>', methods=['GET', 'POST'])
@login_required
def single_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        project.status = request.form['status']

        db.session.commit()
        flash('Project updated successfully.', 'success')
        return redirect(url_for('projects'))

    return render_template('edit_project.html', project=project)

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully.', 'success')
    return redirect(url_for('projects'))

# --- Tasks ---

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        project_id = request.form['project_id']  # assuming this is provided in the form

        new_task = Task(name=name, description=description, status=status, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully.', 'success')
        return redirect(url_for('tasks'))

    tasks = Task.query.filter_by(project_id=project_id).all()  # assuming tasks are tied to a specific project
    return render_template('tasks.html', tasks=tasks)

@app.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()

    if form.validate_on_submit():
        new_task = Task(name=form.name.data, description=form.description.data, status=form.status.data, project_id=form.project_id.data)
        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully.', 'success')
        return redirect(url_for('tasks'))

    return render_template('new_task.html', form=form)

@app.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
@login_required
def single_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        task.status = request.form['status']

        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted successfully.', 'success')
    return redirect(url_for('tasks'))

# --- Trail Systems ---
# Note: I'm assuming a TrailSystem doesn't belong to a specific user

@app.route('/trail_systems', methods=['GET', 'POST'])
@login_required
def trail_systems():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']

        new_trail_system = TrailSystem(name=name, location=location, description=description)
        db.session.add(new_trail_system)
        db.session.commit()

        flash('Trail system added successfully.', 'success')
        return redirect(url_for('trail_systems'))

    trail_systems = TrailSystem.query.all()
    return render_template('trail_systems.html', trail_systems=trail_systems)

@app.route('/new_trail_system', methods=['GET', 'POST'])
@login_required
def new_trail_system():
    form = TrailSystemForm()

    if form.validate_on_submit():
        new_trail_system = TrailSystem(
            name=form.name.data,
            description=form.description.data,
            project_id=form.project_id.data
        )
        db.session.add(new_trail_system)
        db.session.commit()
        flash('New trail system added successfully.', 'success')
        return redirect(url_for('trail_systems'))

    return render_template('new_trail_system.html', form=form)

@app.route('/trail_systems/<int:trail_system_id>', methods=['GET', 'POST'])
@login_required
def single_trail_system(trail_system_id):
    trail_system = TrailSystem.query.get_or_404(trail_system_id)

    if request.method == 'POST':
        trail_system.name = request.form['name']
        trail_system.location = request.form['location']
        trail_system.description = request.form['description']

        db.session.commit()
        flash('Trail system updated successfully.', 'success')
        return redirect(url_for('trail_systems'))

    return render_template('edit_trail_system.html', trail_system=trail_system)

@app.route('/trail_systems/<int:trail_system_id>/delete', methods=['POST'])
@login_required
def delete_trail_system(trail_system_id):
    trail_system = TrailSystem.query.get_or_404(trail_system_id)

    db.session.delete(trail_system)
    db.session.commit()

    flash('Trail system deleted successfully.', 'success')
    return redirect(url_for('trail_systems'))

# --- Expense Reports ---

@app.route('/expense_reports', methods=['GET', 'POST'])
@login_required
def expense_reports():
    if request.method == 'POST':
        date_submitted = request.form['date_submitted']
        amount = request.form['amount']
        description = request.form['description']

        new_expense_report = ExpenseReport(date_submitted=date_submitted, amount=amount, description=description, user_id=current_user.id)
        db.session.add(new_expense_report)
        db.session.commit()

        flash('Expense report added successfully.', 'success')
        return redirect(url_for('expense_reports'))

    expense_reports = ExpenseReport.query.filter_by(user_id=current_user.id).all()
    return render_template('expense_reports.html', expense_reports=expense_reports)

@app.route('/new_expense_report', methods=['GET', 'POST'])
@login_required
def new_expense_report():
    form = ExpenseReportForm()

    if form.validate_on_submit():
        new_expense_report = ExpenseReport(date_submitted=form.date_submitted.data, amount=form.amount.data, description=form.description.data, user_id=current_user.id)
        db.session.add(new_expense_report)
        db.session.commit()

        flash('Expense report added successfully.', 'success')
        return redirect(url_for('expense_reports'))

    return render_template('new_expense_report.html', form=form)

@app.route('/expense_reports/<int:expense_report_id>', methods=['GET', 'POST'])
@login_required
def single_expense_report(expense_report_id):
    expense_report = ExpenseReport.query.get_or_404(expense_report_id)

    if request.method == 'POST':
        expense_report.date_submitted = request.form['date_submitted']
        expense_report.amount = request.form['amount']
        expense_report.description = request.form['description']

        db.session.commit()
        flash('Expense report updated successfully.', 'success')
        return redirect(url_for('expense_reports'))

    return render_template('edit_expense_report.html', expense_report=expense_report)

@app.route('/expense_reports/<int:expense_report_id>/delete', methods=['POST'])
@login_required
def delete_expense_report(expense_report_id):
    expense_report = ExpenseReport.query.get_or_404(expense_report_id)

    db.session.delete(expense_report)
    db.session.commit()

    flash('Expense report deleted successfully.', 'success')
    return redirect(url_for('expense_reports'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables
    app.run(debug=True)