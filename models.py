from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    equipment = db.relationship('Equipment', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    expense_reports = db.relationship('ExpenseReport', backref='user', lazy=True)

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(64), nullable=False)  # New status attribute
    maintenance_schedule = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(64), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trail_system_id = db.Column(db.Integer, db.ForeignKey('trail_systems.id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(64), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

class TrailSystem(db.Model):
    __tablename__ = 'trail_systems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(255))
    map = db.Column(db.LargeBinary)  # Adjust as needed for your method of storing maps
    description = db.Column(db.Text)

    projects = db.relationship('Project', backref='trail_system', lazy=True)

class ExpenseReport(db.Model):
    __tablename__ = 'expense_reports'

    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.Date)
    expense_details = db.Column(db.Text)
    amount = db.Column(db.Numeric(9, 2))  # Decimal for currency
    status = db.Column(db.String(64))  # Adjust as needed

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
