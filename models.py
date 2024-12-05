from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
db = SQLAlchemy(app)

class Auth(db.Model):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    login = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role')

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'))
    task = relationship('Task')
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    auth_id = Column(Integer, ForeignKey('auth.id'))
    auth = relationship('Auth')

class Role(db.Model):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Task(db.Model):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    head = Column(String(100), nullable=False)
    status = Column(Integer, ForeignKey('status.id'))
    status = relationship('Status')
    type = Column(Integer, ForeignKey('type.id'))
    type = relationship('Type')
    description = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    name_client = Column(String(100), nullable=False)
    executor = Column(Integer)
    beg_date = Column(DateTime)
    end_date = Column(Date)
    id_priority = Column(Integer, ForeignKey('priority.id'))
    priority = relationship('Priority')

class Priority(db.Model):
    __tablename__ = 'priority'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Status(db.Model):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Type(db.Model):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

with app.app_context():
    db.create_all()