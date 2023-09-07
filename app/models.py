from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    position = db.Column(db.String(100))  # You can adjust the length as needed

    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __init__(self, user_id, comment, position):
        self.user_id = user_id
        self.comment = comment
        self.position = position