from app import db
from dataclasses import dataclass

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username=None, email=None, type=None, password=None):
        self.username = username
        self.email = email
        self.type = type
        self.password = password


    def __repr__(self):
        return '<User %r>' % (self.username)     