from .model import User

def get_user_info(user_id):
    look = User.query.filter(User.id==user_id).first()

    return look