from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    banner_image = db.Column(db.String(100), nullable=True)  # store image filename or URL

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    client = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Not Started')
    deadline = db.Column(db.Date)
    description = db.Column(db.Text)
    poc_name = db.Column(db.String(100))
    poc_email = db.Column(db.String(100))
    poc_number = db.Column(db.String(100))
    poc_role = db.Column(db.String(100))
    github_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ProjectUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    update_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100))  # Optional: who made the update

    project = db.relationship('Project', backref=db.backref('updates', lazy=True))