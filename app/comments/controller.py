from flask import Blueprint, request, jsonify
from app import db
from app.comments.model import Comment
from app.cards.model import Card
from app.users.role_checker import get_user_info

comment = Blueprint('comment', __name__, url_prefix='/api/v1/comments')

@comment.route('/', methods=['GET'])
def index():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    card_id = request.args.get('card_id')
    list_data = Comment.query.filter(Comment.card_id==card_id).paginate(int(page), int(per_page), False)
    total = list_data.total
    items = list_data.items

    res = []

    for data in items:
        res.append({'id': data.id, 'body': data.body, 'card_id': data.card_id, 'is_replay_from': data.is_reply_from, 'list_id': data.list_id})

    return jsonify(message="success", data=res, records=total)

@comment.route('/create/', methods=['POST'])
def create():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    req = request.form
    is_reply_from = req['is_reply_from'] if req['is_reply_from'] else None
    
    data = Comment(body=req['body'], list_id=req['list_id'], card_id=req['card_id'], is_reply_from=is_reply_from, created_by=user_id)

    db.session.add(data)
    db.session.commit()

    db.session.query(Card).filter(Card.id == data.id).update({'comment_count': Card.comment_count + 1})
    db.session.commit()

    res = {'id': data.id,'body': data.body, 'list_id': data.list_id, 'card_id': data.card_id, 'list_id': data.list_id, 'is_reply_from': data.is_reply_from}

    return jsonify(message="success", data=res)

@comment.route('/show/<id>/', methods=['GET'])
def show(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']

    data = Comment.query.filter(Comment.id==id).first()   

    if not data:
        return jsonify(message='No data found.'), 422

    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    list_data = Comment.query.filter(Comment.is_reply_from==data.id).paginate(int(page), int(per_page), False)
    total = list_data.total
    items = list_data.items

    data_list = []

    for reply in items:
        data_list.append({'id': reply.id, 'title': reply.body, 'list_id': reply.list_id, 'card_id': reply.card_id, 'is_reply_from': reply.is_reply_from})

    res = {'id': data.id,'body': data.title, 'reply_list': data_list}

    return jsonify(message='success', data=res)

@comment.route('/update/<id>/', methods=['POST'])
def update(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']
    req = request.form

    check = Comment.query.filter(Comment.id==id).first()

    if str(check.created_by) != str(user_id):
        return jsonify(message="You cannot update a comment which is not belong to you."), 422 

    if check:
        db.session.query(Comment).filter(Comment.id == id).update({'body': req['body']})
        db.session.commit()

        return jsonify(message="successfully updated.")

    return jsonify(message="No data found."), 422 

@comment.route('/delete/<id>/', methods=['POST'])
def delete(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']
    req = request.form

    check = Comment.query.filter(Comment.id==id).first()

    if str(check.created_by) != str(user_id):
        return jsonify(message="You cannot delete a comment which is not belong to you."), 422 

    if check:
        db.session.query(Comment).filter(Comment.id == id).delete()
        db.session.commit()

        db.session.query(Card).filter(Card.id == check.card_id).update({'comment_count': Card.comment_count - 1})
        db.session.commit()

        return jsonify(message="successfully deleted.")