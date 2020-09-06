from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app import db
from .model import User

user = Blueprint('user', __name__, url_prefix='/api/v1/users')

@user.route('/', methods=['GET'])
def index():
    per_page = 20
    page = request.args.get('page') if request.args.get('page') else 0
    users = User.query.paginate(int(page), int(per_page), False)
    total = users.total
    items = users.items

    res = []

    for data in items:
        res.append({'id': data.id, 'username': data.username, 'email': data.email, 'type': data.type})

    return jsonify(message="success", data=res, records=total)

@user.route('/create/', methods=['POST'])
def create():
    req = request.form

    check = User.query.filter(User.email==req['email']).first()

    if check:
        return jsonify(message="Email Already Taken"), 422 
    
    data = User(username=req['username'], email=req['email'], type=req['type'], password=generate_password_hash(req['password']))

    db.session.add(data)
    db.session.commit()

    res = {'id': data.id,'username': data.username, 'email': data.email, 'type': data.type}

    return jsonify(message="success", data=res)

@user.route('/show/<id>/', methods=['GET'])
def show(id):
    id = request.view_args['id']

    data = User.query.filter(User.id==id).first()
    
    if not data:
        return jsonify(message='No data found.'), 422

    res = {'id': data.id,'username': data.username, 'email': data.email, 'type': data.type}

    return jsonify(message='success', data=res)

@user.route('/update/<id>/', methods=['POST'])
def update(id):
    id = request.view_args['id']
    req = request.form

    check = User.query.filter(User.id==id).first()

    if check:
    
        data = User(username=req['username'], email=req['email'], type=req['type'], password=req['password'])

        db.session.update(data)
        db.session.commit()

        res = {'id': data.id,'username': data.username, 'email': data.email, 'type': data.type}

        return jsonify(message="success", data=res)
    

    res = {'id': check.id,'username': check.username, 'email': check.email, 'type': check.type}
    return jsonify(message="No data found."), 422 

@user.route('/delete/', methods=['POST'])
def delete():
    return ''