from flask_wtf import FlaskForm
from models import TrailSystem, Project
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, DateField, SelectField, DecimalField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('completed', 'Completed'), ('on hold', 'On Hold')])
    trail_system_id = SelectField('Trail System', coerce=int)  # dropdown field to select the Trail System
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.trail_system_id.choices = [(ts.id, ts.name) for ts in TrailSystem.query.all()]

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('not started', 'Not Started')])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(p.id, p.name) for p in Project.query.all()]

class TrailSystemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    map = FileField('Upload Map', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDFs only!')])
    submit = SubmitField('Submit')

class EditTrailSystemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    map = FileField('Upload Map', validators=[FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDFs only!')])
    submit = SubmitField('Submit')

class ExpenseReportForm(FlaskForm):
    date_submitted = StringField('Date', validators=[DataRequired()], render_kw={'type': 'date'})  # For input type date
    amount = DecimalField('Amount', validators=[DataRequired()])  # Decimal for currency
    expense_details = TextAreaField('Details', validators=[DataRequired()])
    status = SelectField('Status', choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('denied', 'Denied')]) 
    submit = SubmitField('Submit')

class EquipmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('maintenance', 'Maintenance'), ('out of order', 'Out of Order')]) 
    maintenance_schedule = StringField('Maintenance Schedule', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    old_password = PasswordField('Old Password')
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')