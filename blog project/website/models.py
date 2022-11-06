from cgitb import text
import email
from time import timezone
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.column(db.String(120), unique= True)
    password = db.column(db.String(120), unique= True)
    date_created = db.column(db.DateTimes(timezone= True), default = func.now())
    posts= db.relationship('Post', backref= 'user', passive_deletes=True)

class Post(db.Model):
    id= db.column(db.Integer, primary_key=True)
    text = db.column(db.Text, nullable= False)
    date_created = db.Column(db.DateTime(timezone= True), default = func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', undelete="CASCADE", nullable = False))
    