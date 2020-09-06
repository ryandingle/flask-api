from flask import Blueprint, request, jsonify
from app import db
from .model import Card
from app.list.model import List
from app.comments.model import Comment
from app.users.role_checker import get_user_info
from sqlalchemy.orm import sessionmaker

import config

engine = config.SQLALCHEMY_DATABASE_URI
Session = sessionmaker(bind = engine)
session = Session()

card = Blueprint('card', __name__, url_prefix='/api/v1/cards')

@card.route('/', methods=['GET', 'POST'])
def index():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    list_data = Card.query.order_by(Card.comment_count.desc()).paginate(int(page), int(per_page), False)

    total = list_data.total
    items = list_data.items

    res = []

    for data in items:
        res.append({'id': data.id, 'title': data.title, 'list_id': data.list_id, 'description': data.description, 'comment_count': data.comment_count})

    return jsonify(message="success", data=res, records=total)

@card.route('/create/', methods=['POST'])
def create():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    req = request.form

    check = Card.query.filter(List.title==req['title']).first()

    if check:
        return jsonify(message="Card Title Already Taken"), 422 
    
    data = Card(title=req['title'], description=req['description'], list_id=req['list_id'], created_by=user_id)

    db.session.add(data)
    db.session.commit()

    res = {'id': data.id,'title': data.title, 'description': data.description, 'list_id': data.list_id}

    return jsonify(message="success", data=res)

@card.route('/show/<id>/', methods=['GET'])
def show(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']

    data = Comment.query.filter(List.id==id).first()

    list_data = Comment.query.filter(Comment.card_id==req['card_id'])[:3]

    data_list = []

    for comments in list_data:
        data_list.append({'id': comments.id, 'body': comments.body, 'card_id': comments.card_id, 'list_id': comments.list_id})
    
    if not data:
        return jsonify(message='No data found.'), 422

    res = {'id': data.id,'title': data.title, 'description': data.description, 'cards': data_list}

    return jsonify(message='success', data=res)

@card.route('/update/<id>/', methods=['POST'])
def update(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']
    req = request.form

    check = Card.query.filter(Card.id==id).first()

    if str(check.created_by) != str(user_id):
        return jsonify(message="You cannot update a card which is not belong to you."), 422 

    if check:
        db.session.query(Card).filter(Card.id == id).update({'title': req['title'], 'description': req['description']})
        db.session.commit()

        return jsonify(message="successfully updated.")

    return jsonify(message="No data found."), 422 

@card.route('/delete/<id>/', methods=['POST'])
def delete(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']
    req = request.form

    check = Card.query.filter(Card.id==id).first()

    if str(check.created_by) != str(user_id):
        return jsonify(message="You cannot delete a card which is not belong to you."), 422 

    if check:
        db.session.query(Comment).filter(Comment.card_id == id).delete()
        db.session.commit()

        db.session.query(Card).filter(Card.id == id).delete()
        db.session.commit()

        return jsonify(message="successfully deleted.")

    return jsonify(message="No data found."), 422 