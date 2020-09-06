from flask import Flask, render_template

# Import SQLAlchemy
# from flask import sqlalchemy as SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskexam.sqlite"

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    # return render_template('404.html'), 404
    return error, 404

@app.route('/', methods=['GET'])
def index():
    return 'Hello Word!'

from app.auth.controller import auth as auth_module
from app.users.controller import user as user_module
from app.cards.controller import card as comment_module
from app.comments.controller import comment as card_module
from app.list.controller import list as list_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(user_module)
app.register_blueprint(comment_module)
app.register_blueprint(card_module)
app.register_blueprint(list_module)

db.create_all()