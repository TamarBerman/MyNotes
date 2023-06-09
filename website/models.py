from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    """Schema for a note"""
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    '''One-to-many relationship, - one user has many notes'''
    '''p.s. lowercase in foreign key'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    """Schema for a user"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    '''all user's personal notes'''
    '''every time i add a note, it adds his own id to that list'''
    '''uppercase letter in relationship'''
    notes = db.relationship('Note')
