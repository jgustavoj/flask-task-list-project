from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime as dt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.email


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean(), nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=dt.datetime.now())
    due_date = db.Column(db.DateTime, default=dt.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, task, due_date, user_id):
        self.task = task 
        self.due_date = due_date
        self.user_id = user_id

    def __repr__(self):
        return '<Todo %r>' % self.id

  
