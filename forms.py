from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('completed', 'Completed'), ('on hold', 'On Hold')]) 
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('not started', 'Not Started')])
    submit = SubmitField('Submit')

class TrailSystemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    map = FileField('Upload Map', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])  # This is assuming that maps are image files.
    submit = SubmitField('Submit')

class ExpenseReportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_submitted = StringField('Date', validators=[DataRequired()])  # For input type date
    amount = DecimalField('Amount', validators=[DataRequired()])  # Changed from cost to amount to match model
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('denied', 'Denied')]) 
    submit = SubmitField('Submit')