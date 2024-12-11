from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
db = SQLAlchemy(app)

class Auth(db.Model):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(30), nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role')

    def assign_role(self, role_name):
        """Назначить роль пользователю"""
        role = Role.query.filter_by(name=role_name).first()
        if role:
            self.role = role
            db.session.commit()

    def remove_role(self):
        """Удалить роль у пользователя"""
        self.role = None
        db.session.commit()

    def has_role(self, role_name):
        """Проверить, есть ли у пользователя указанная роль"""
        return self.role and self.role.name == role_name


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

    '''@staticmethod
    def add_roles():
        """Добавить несколько ролей в базу данных"""
        # Создаем объекты ролей
        admin_role = Role(name="admin")
        user_role = Role(name="user")
        
        # Добавляем их в сессию
        db.session.add(admin_role)
        db.session.add(user_role)
        
        # Сохраняем в базе данных
        db.session.commit()
        print("Роли добавлены в базу данных.")'''

class Task(db.Model):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    head = Column(String(100), nullable=False)
    name = Column(String(100), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'))  # status_id указывает на id в статусе
    status = relationship('Status', backref='tasks')  # Используйте 'backref', чтобы упростить связь с Task
    type = Column(Integer, ForeignKey('type.id'))
    description = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
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

    #db.session.commit()

with app.app_context():
    db.create_all()
    #role1 = Role(name = 'admin')
    #role2 = Role(name = 'user')
    #db.session.add(role1)
    #db.session.add(role2)
    db.session.commit()