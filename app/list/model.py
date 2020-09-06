from app import db
from dataclasses import dataclass

class List(db.Model):
    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    assigned_member = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer, nullable=False)

    def __init__(self, title=None, assigned_member=None, created_by=None):
        self.title = title
        self.assigned_member = assigned_member
        self.created_by = created_by

    def __repr__(self):
        return '<List %r>' % (self.title)     