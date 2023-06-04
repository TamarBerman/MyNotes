from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')




# from . import db
# from flask_login import UserMixin
# from sqlalchemy import func
#
#
# # סכמה לשמירת פוסט
# class Note(db.Model):
#     id = db.Column(db.Integer, primery_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     # קשר של יחיד לרבים- למשתמש אחד יש פוסטים רבים
#     # אות קטנה במפתח זר
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#
# # סכמה לשמירת המשתמש בDB
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primery_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     #    הפוסטים שהוא יצר לכל משתמש - את כל
#     # בכל פעם שאני מוסיף פוסט- תוסיף את הID שלו לרשימה הזו
#     # אות גדולה בקשר
#     nots = db.relationship('Note')
#
