from app import db
from dataclasses import dataclass

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    comment_count = db.Column(db.Integer, nullable=False, default=0)
    created_by = db.Column(db.Integer, nullable=False)

    def __init__(self, title=None, list_id=None, description=None, comment_count=None, created_by=None):
        self.title = title
        self.list_id = list_id
        self.description = description
        self.comment_count = comment_count
        self.created_by = created_by

    def __repr__(self):
        return '<Card %r>' % (self.title)     