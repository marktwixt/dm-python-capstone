import os
import sqlalchemy as sa
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Project, Task, Equipment, TrailSystem, ExpenseReport, db
from app import login_manager, app
from forms import LoginForm, EditTrailSystemForm, RegistrationForm, UserProfileForm, ProjectForm, TaskForm, TrailSystemForm, ExpenseReportForm, EquipmentForm
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import datetime
from werkzeug.utils import secure_filename

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

# --- Registration/Login/Logout/Users ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/users', methods=['GET'])
@login_required
def users():
    user_list = User.query.all()
    return render_template('users.html', users=user_list)

@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = UserProfileForm()
    if form.validate_on_submit():
        # Check the old password if it is entered
        if form.old_password.data and bcrypt.check_password_hash(user.password, form.old_password.data):
            # update profile details
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data

            # Only update the password if a new one is entered
            if form.password.data:
                user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # if picture field is not empty, save the picture
            if form.picture.data:
                picture_file = secure_filename(form.picture.data.filename)
                picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file)
                form.picture.data.save(picture_path)
                user.profile_image = picture_file

            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('user_profile', user_id=user.id))
        elif form.old_password.data:
            flash('Wrong current password.', 'danger')
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.bio.data = user.bio
    return render_template('user_profile.html', user=user, form=form)

# --- Equipment ---

@app.route('/equipment', methods=['GET'])
@login_required
def equipment():
    form = EquipmentForm()
    equipment_list = Equipment.query.all()
    return render_template('equipment.html', form=form, equipment_list=equipment_list)

@app.route('/equipment/new', methods=['GET', 'POST'])
@login_required
def new_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        new_equipment = Equipment(
            name=form.name.data,
            description=form.description.data,
            status=form.status.data,
            maintenance_schedule=form.maintenance_schedule.data,
            user_id=current_user.id
        )
        db.session.add(new_equipment)
        db.session.commit()
        flash('Equipment added successfully.', 'success')
        return redirect(url_for('equipment'))
    return render_template('new_equipment.html', form=form)

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

@app.route('/projects', methods=['GET'])
@login_required
def projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=projects)

@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    trail_systems = [(ts.id, ts.name) for ts in TrailSystem.query.all()] # get a list of all trail systems
    form = ProjectForm(request.form)
    form.trail_system_id.choices = trail_systems # set the choices for the trail_system_id field
    if form.validate_on_submit():
        new_project = Project(name=form.name.data, description=form.description.data, status=form.status.data, user_id=current_user.id, trail_system_id=form.trail_system_id.data)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully.', 'success')
        return redirect(url_for('projects'))
    return render_template('new_project.html', form=form)

@app.route('/projects/<int:project_id>', methods=['GET', 'POST'])
@login_required
def single_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        if form.status.data:  # Check if a status was selected
            project.status = form.status.data

        db.session.commit()
        flash('Project updated successfully.', 'success')
        return redirect(url_for('projects'))

    return render_template('edit_project.html', form=form, project=project)

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully.', 'success')
    return redirect(url_for('projects'))

# --- Tasks ---

@app.route('/tasks', methods=['GET'])
@login_required
def tasks():
    form = TaskForm()
    tasks = Task.query.all() # Fetch all tasks, not filtered by project_id
    return render_template('tasks.html', tasks=tasks, form=form)

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
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.status = form.status.data

        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', task=task, form=form)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted successfully.', 'success')
    return redirect(url_for('tasks'))

# --- Trail Systems ---
@app.route('/trail_systems', methods=['GET'])
@login_required
def trail_systems():
    trail_systems = TrailSystem.query.all()
    return render_template('trail_systems.html', trail_systems=trail_systems)

@app.route('/new_trail_system', methods=['GET', 'POST'])
@login_required
def new_trail_system():
    form = TrailSystemForm()

    if form.validate_on_submit():
        f = form.map.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_trail_system = TrailSystem(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            map=filename
        )
        db.session.add(new_trail_system)
        db.session.commit()

        flash('New trail system added successfully.', 'success')
        return redirect(url_for('trail_systems')) 
    else:
        print("Form data:", form.data)
        print("Form errors:", form.errors)
    return render_template('new_trail_system.html', form=form)

@app.route('/trail_systems/<int:trail_system_id>', methods=['GET', 'POST'])
@login_required
def single_trail_system(trail_system_id):
    trail_system = TrailSystem.query.get_or_404(trail_system_id)
    form = EditTrailSystemForm(obj=trail_system)

    if form.validate_on_submit():
        trail_system.name = form.name.data
        trail_system.location = form.location.data
        trail_system.description = form.description.data

        f = request.files.get('map')
        if f:
            # A new file has been uploaded
            if trail_system.map:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], trail_system.map))
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            trail_system.map = filename
        db.session.commit()
        flash('Trail system updated successfully.', 'success')
        return redirect(url_for('trail_systems'))
    return render_template('edit_trail_system.html', trail_system=trail_system, form=form)

@app.route('/trail_systems/<int:trail_system_id>/delete', methods=['POST'])
@login_required
def delete_trail_system(trail_system_id):
    trail_system = TrailSystem.query.get_or_404(trail_system_id)
    
    # delete the associated file
    if trail_system.map:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], trail_system.map)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(trail_system)
    db.session.commit()

    flash('Trail system deleted successfully.', 'success')
    return redirect(url_for('trail_systems'))

# --- Expense Reports ---

@app.route('/new_expense_report', methods=['GET', 'POST'])
@login_required
def new_expense_report():
    form = ExpenseReportForm()
    if form.validate_on_submit():
        new_expense_report = ExpenseReport(date_submitted=form.date_submitted.data, amount=form.amount.data, expense_details=form.expense_details.data, status='submitted', user_id=current_user.id)
        db.session.add(new_expense_report)
        db.session.commit()
        flash('Expense report submitted successfully.', 'success')
        return redirect(url_for('expense_reports'))
    return render_template('new_expense_report.html', form=form)

@app.route('/expense_reports/<int:expense_report_id>', methods=['GET', 'POST'])
@login_required
def single_expense_report(expense_report_id):
    expense_report = ExpenseReport.query.get_or_404(expense_report_id)
    form = ExpenseReportForm()

    if form.validate_on_submit():
        expense_report.date_submitted = form.date_submitted.data
        expense_report.amount = form.amount.data
        expense_report.expense_details = form.expense_details.data
        expense_report.status = form.status.data

        db.session.commit()
        flash('Expense report updated successfully.', 'success')
        return redirect(url_for('expense_reports'))

    if request.method == 'GET':
        form.date_submitted.data = expense_report.date_submitted
        form.amount.data = expense_report.amount
        form.expense_details.data = expense_report.expense_details
        form.status.data = expense_report.status

    return render_template('edit_expense_report.html', form=form)

@app.route('/expense_reports', methods=['GET'])
@login_required
def expense_reports():
    expense_reports = ExpenseReport.query.filter_by(user_id=current_user.id).all()
    return render_template('expense_reports.html', reports=expense_reports)

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
        db.create_all()
    app.run(debug=True)