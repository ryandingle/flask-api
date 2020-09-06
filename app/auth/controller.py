from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.users.model import User
from datetime import datetime

import base64

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/signin/', methods=['POST'])
def signin():
    user = User.query.filter_by(email=request.form['email']).first()

    string = str(datetime.now())
    encodedBytes = base64.b64encode(string.encode("utf-8"))
    token = str(encodedBytes, "utf-8")

    if user and check_password_hash(user.password, request.form['password']):

        return jsonify(message="success", token=token)

    return jsonify(message="Invalid Credentials."), 422