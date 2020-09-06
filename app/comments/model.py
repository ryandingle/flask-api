from app import db
from dataclasses import dataclass

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, nullable=False)
    card_id = db.Column(db.Integer, nullable=False)
    is_reply_from = db.Column(db.Integer, nullable=True)
    body = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    def __init__(self, title=None, list_id=None, card_id=None, body=None, is_reply_from=None, created_by=None):
        self.title = title
        self.list_id = list_id
        self.card_id = card_id
        self.body = body
        self.is_reply_from = is_reply_from
        self.created_by = created_by

    def __repr__(self):
        return '<Comment %r>' % (self.body)     