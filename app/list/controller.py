from flask import Blueprint, request, jsonify
from app import db
from .model import List
from app.cards.model import Card
from app.users.role_checker import get_user_info

list = Blueprint('list', __name__, url_prefix='/api/v1/lists')

@list.route('/', methods=['GET'])
def index():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    list_data = List.query.paginate(int(page), int(per_page), False)

    if user_info.type == 'member':
        list_data = List.query.filter(List.assigned_member==user_id).paginate(int(page), int(per_page), False)

    total = list_data.total
    items = list_data.items

    res = []

    for data in items:
        res.append({'id': data.id, 'title': data.title, 'assigned_member': data.assigned_member})

    return jsonify(message="success", data=res, records=total)

@list.route('/create/', methods=['POST'])
def create():
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)

    if user_info.type == 'member':
        return jsonify(message="Not authorized"), 422 

    req = request.form

    check = List.query.filter(List.title==req['title']).first()

    if check:
        return jsonify(message="Title Already Taken"), 422 
    
    data = List(title=req['title'], created_by=user_id)

    db.session.add(data)
    db.session.commit()

    res = {'id': data.id,'title': data.title, 'assigned_member': data.assigned_member}

    return jsonify(message="success", data=res)

@list.route('/show/<id>/', methods=['GET'])
def show(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)
    id = request.view_args['id']

    data = List.query.filter(List.id==id).first()
    
    if not data:
        return jsonify(message='No data found.'), 422

    if user_info.type == 'member' and str(data.assigned_member) != str(user_id):
        return jsonify(message="Not authorized."), 422 

    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    list_data = Card.query.filter(Card.list_id==id).paginate(int(page), int(per_page), False)
    total = list_data.total
    items = list_data.items

    card_list = []

    for card in items:
        card_list.append({'id': card.id, 'title': card.title, 'assigned_member': card.assigned_member})

    res = {'id': data.id,'title': data.title, 'cards': card_list}

    return jsonify(message='success', data=res)

@list.route('/update/<id>/', methods=['POST'])
def update(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)

    if user_info.type == 'member':
        return jsonify(message="Not authorized"), 422 

    id = request.view_args['id']
    req = request.form

    check = List.query.filter(List.id==id).first()

    if check:
        db.session.query(List).filter(List.id == id).update({'title': req['title']})
        db.session.commit()

        return jsonify(message="successfully updated.")

    return jsonify(message="No data found."), 422 

@list.route('/member_assignment/<id>/', methods=['POST'])
def member_assignment(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)

    if user_info.type == 'member':
        return jsonify(message="Not authorized"), 422 

    id = request.view_args['id']
    req = request.form

    check = List.query.filter(List.id==id).first()

    if check:
        if req['action'] == 'assign':
            db.session.query(List).filter(List.id == id).update({'assigned_member': req['member_id']})

        if req['action'] == 'unassign':
            db.session.query(List).filter(List.id == id).update({'assigned_member': None})

        db.session.commit()

        return jsonify(message="successfully updated.")

    return jsonify(message="No data found."), 422

@list.route('/delete/<id>/', methods=['POST'])
def delete(id):
    user_id = request.args.get('user_id')
    user_info = get_user_info(user_id)

    if user_info.type == 'member':
        return jsonify(message="Not authorized"), 422 

    id = request.view_args['id']
    req = request.form

    check = List.query.filter(List.id==id).first()

    if str(check.created_by) != str(user_id):
        return jsonify(message="You cannot delete a list which is not belong to you."), 422 

    if check:
        db.session.query(Card).filter(Card.list_id == id).delete()
        db.session.commit()

        db.session.query(List).filter(List.id == id).delete()
        db.session.commit()

        return jsonify(message="successfully deleted.")

    return jsonify(message="No data found."), 422 